"""Read and search the installed guides. No application or provider imports."""

from dataclasses import dataclass
from html import escape
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt


@dataclass(frozen=True)
class Guide:
    slug: str
    source: str
    title: str
    description: str
    group: str
    keywords: str = ""

    @property
    def href(self) -> str:
        return f"/studio/guides/{self.slug}"


GUIDES = (
    Guide("quick-start", "docs/QUICKSTART.md", "Get started", "Open the app, try the example, and prepare your first chain.", "Start here", "install first launch beginner"),
    Guide("getting-more", "docs/GETTING-THE-MOST-OUT-OF-IT.md", "Get more out of a session", "Give a thought a useful destination and improve the handoffs.", "Start here", "better results quality prompts context"),
    Guide("recipes", "docs/RECIPE-GUIDE.md", "Choose a recipe", "Find the right method for what you want to leave with.", "Start here", "explain write decide learn connect untangle"),
    Guide("examples", "docs/WORKED-EXAMPLES.md", "Follow a worked example", "Walk through learning, drafting, and finding a next action.", "Start here", "moon walkthrough tutorial"),
    Guide("professional-cases", "docs/PROFESSIONAL-CASES.md", "Practice a professional workflow", "Review a decision memo, evidence brief, or document before handing it over.", "Make it yours", "practice decision memo evidence brief document review source packet"),
    Guide("building-chains", "docs/CHAIN-BUILDING.md", "Build your own chains", "Connect prompts and answers, with a complete three-step recipe.", "Make it yours", "placeholders variables output custom JSON"),
    Guide("accessibility", "docs/DAILY-USE-AND-ACCESSIBILITY.md", "Less typing, easier return", "Use dictation, shortcuts, saved methods, and small sessions.", "Make it yours", "keyboard dictation aliases drafts resume"),
    Guide("setup", "docs/SETUP-AND-MODELS.md", "Setup and models", "Configure generation, choose a model, and understand limits.", "Keep it working", "key OpenRouter tokens temperature timeout cost install port"),
    Guide("saving-and-recovery", "docs/SAVING-EXPORT-AND-RECOVERY.md", "Save, export, and recover", "Keep the right record, back it up, and pick up interrupted work.", "Keep it working", "backup restore library paused failed interrupted Markdown JSON"),
    Guide("troubleshooting", "docs/TROUBLESHOOTING.md", "Resolve a problem", "Find the next useful check for an error or unexpected behavior.", "Keep it working", "error failed stuck missing rejected doctor"),
    Guide("advanced-tools", "docs/ADVANCED-TOOLS.md", "Use the advanced tools", "Explore reasoning patterns, debate, meta-chains, and artifacts.", "Reference", "Python API framework"),
    Guide("documentation-map", "docs/README.md", "Documentation map", "The complete reading map included with this project.", "Reference"),
    Guide("project-overview", "README.md", "Project overview", "The project's overview, commands, and operating boundaries.", "Reference"),
    Guide("roadmap", "ROADMAP.md", "Project roadmap", "The phased direction and deliberately deferred scope.", "Reference"),
    Guide("architecture", "docs/ARCHITECTURE.md", "How the app is built", "Understand the modules, persistence, and execution boundaries.", "Reference", "SQLite Chroma developer architecture"),
    Guide("testing", "docs/TESTING.md", "Verification reference", "Distinguish offline tests, provider checks, and human acceptance.", "Reference", "test pytest checks"),
    Guide("status", "docs/WORKBENCH-STATUS.md", "Implementation status", "Read what was implemented and which checks were performed.", "Reference"),
    Guide("demos", "docs/DEMOS.md", "Teach with a classroom challenge", "Lead a class through the clues, the draft, and the next prompt.", "Reference", "classroom teacher practice offline demos"),
    Guide("legacy-demos", "docs/LEGACY-DEMOS.md", "Earlier framework demos", "Historical walkthroughs for the previous interface.", "Earlier notes"),
    Guide("ideas", "docs/IDEAS.md", "Earlier ideas", "The historical inventory of project ideas and proposals.", "Earlier notes"),
    Guide("changelog", "docs/CHANGELOG.md", "Historical changelog", "Earlier development changes.", "Earlier notes"),
    Guide("release-notes", "docs/WHATS_NEW.md", "Earlier release notes", "Notes describing previous versions of the framework.", "Earlier notes"),
)

SEARCH_ALIASES = {
    "placeholders": "placeholder",
    "rca": "root cause",
    "voice": "dictation",
    "speech to text": "dictation",
}


@dataclass
class Section:
    title: str
    anchor: str
    level: int
    text: str = ""


@dataclass
class Document:
    guide: Guide
    title: str
    html: str
    source: str
    sections: list[Section]


@dataclass
class SearchHit:
    guide: Guide
    excerpt: str
    section: Section
    score: int

    @property
    def href(self) -> str:
        return self.guide.href + (f"#{self.section.anchor}" if self.section.anchor else "")


class GuideUnavailable(ValueError):
    """A known guide cannot currently be read safely."""


class GuideBook:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.guides = {guide.slug: guide for guide in GUIDES}
        self.sources = {self.root / guide.source: guide for guide in GUIDES}

    def _path(self, guide: Guide) -> Path:
        candidate = self.root / guide.source
        # A guide filename must not become an alias for credentials or another
        # file, even if a symlink stays inside the project directory.
        try:
            valid = candidate.resolve() == candidate and candidate.is_file()
        except (OSError, RuntimeError):
            valid = False
        if not valid:
            raise GuideUnavailable("This guide is not available in this installation.")
        return candidate

    def available(self) -> list[Guide]:
        result = []
        for guide in GUIDES:
            try:
                self._path(guide)
                result.append(guide)
            except (OSError, GuideUnavailable):
                continue
        return result

    def href(self, current: Guide, target: str) -> tuple[str | None, bool]:
        """Rewrite known local Markdown links; never expose arbitrary files."""
        try:
            url = urlsplit(target)
            if url.scheme:
                if url.scheme.lower() not in {"http", "https"}:
                    return None, False
                if url.hostname in {"localhost", "127.0.0.1", "::1"} and url.port in {None, 8000}:
                    path = url.path or "/"
                    if self._app_path(path) and url.username is None and url.password is None:
                        return urlunsplit(("", "", path, url.query, url.fragment)), False
                    return None, False
                return target, True
            if url.netloc or target.startswith("//"):
                return None, False
            if not url.path:
                return ("#" + url.fragment) if url.fragment else "#main", False
            if self._app_path(url.path):
                return target, False
            path = (self.root / Path(current.source).parent / unquote(url.path)).resolve()
            guide = self.sources.get(path)
            if guide is None:
                return None, False
            self._path(guide)
            return guide.href + ("#" + url.fragment if url.fragment else ""), False
        except (ValueError, OSError, RuntimeError):
            return None, False

    @staticmethod
    def _app_path(path: str) -> bool:
        return (path == "/" or path.startswith("/studio/")) and "\\" not in unquote(path)

    @staticmethod
    def _plain(inline) -> str:
        return "".join(child.content if child.type in {"text", "code_inline", "image"} else " " if child.type in {"softbreak", "hardbreak"} else "" for child in (inline.children or []))

    @staticmethod
    def _code(tokens, index, _options, env) -> str:
        token = tokens[index]
        language = token.info.strip().split()[0] if token.info.strip() else "text"
        language = language if re.fullmatch(r"[\w+-]{1,30}", language) else "text"
        env["code_index"] = env.get("code_index", 0) + 1
        label = "Copy command" if language in {"bash", "sh", "shell"} else "Copy text" if language in {"text", "dotenv"} else "Copy code"
        return (f'<div class="guide-code" data-copy-scope><div class="guide-code-bar"><span>{escape(language)}</span>'
                f'<button type="button" class="quiet-button" data-copy-nearest="pre" aria-label="{label}, block {env["code_index"]}">{label}</button></div>'
                f'<pre><code>{escape(token.content)}</code></pre></div>\n')

    def read(self, slug: str) -> Document:
        guide = self.guides.get(slug)
        if guide is None:
            raise GuideUnavailable("That guide was not found.")
        try:
            with self._path(guide).open("rb") as stream:
                raw = stream.read(2_000_001)
            if len(raw) > 2_000_000:
                raise GuideUnavailable("This guide is too large to display.")
            source = raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise GuideUnavailable("This guide could not be read. Your saved work is unaffected.") from exc

        markdown = MarkdownIt("commonmark", {"html": False, "linkify": False}).enable("table")
        markdown.renderer.rules["fence"] = self._code
        markdown.renderer.rules["code_block"] = self._code
        markdown.renderer.rules["table_open"] = lambda *_: '<div class="guide-table" role="region" aria-label="Guide table" tabindex="0"><table>\n'
        markdown.renderer.rules["table_close"] = lambda *_: '</table></div>\n'
        markdown.renderer.rules["image"] = lambda ts, i, _opts, _env: f'<span class="guide-image-note">{escape(ts[i].content)}</span>'
        tokens = markdown.parse(source)
        title = guide.title
        if len(tokens) >= 3 and tokens[0].type == "heading_open" and tokens[0].tag == "h1":
            title = self._plain(tokens[1])
            tokens = tokens[3:]
        sections = [Section(title, "", 1)]
        used_ids = {"main", "guide-title"}
        suffixes: dict[str, int] = {}

        for index, token in enumerate(tokens):
            if token.type == "heading_open" and index + 1 < len(tokens):
                heading = self._plain(tokens[index + 1])
                base = re.sub(r"\s+", "-", "".join(ch for ch in heading.casefold() if ch.isalnum() or ch in " _-").strip()) or "section"
                count = suffixes.get(base, 0)
                anchor = base if count == 0 else f"{base}-{count}"
                while anchor in used_ids:
                    count += 1
                    anchor = f"{base}-{count}"
                used_ids.add(anchor)
                suffixes[base] = count + 1
                token.attrSet("id", anchor)
                if token.tag in {"h2", "h3"}:
                    sections.append(Section(heading, anchor, int(token.tag[1])))
            if token.type == "inline":
                sections[-1].text += " " + self._plain(token)
                stack = []
                for child in token.children or []:
                    if child.type == "link_open":
                        href, external = self.href(guide, child.attrGet("href") or "")
                        stack.append(href is not None)
                        if href is None:
                            child.tag, child.attrs = "span", {"class": "guide-unavailable-link"}
                        else:
                            child.attrSet("href", href)
                            if external:
                                child.attrSet("target", "_blank")
                                child.attrSet("rel", "noopener noreferrer")
                    elif child.type == "link_close" and stack:
                        if not stack.pop():
                            child.tag = "span"
            elif token.type in {"fence", "code_block"}:
                sections[-1].text += " " + token.content
        return Document(guide, title, markdown.renderer.render(tokens, markdown.options, {}), source, sections)

    def search(self, query: str) -> list[SearchHit]:
        phrase = " ".join(query.casefold().split())
        phrase = SEARCH_ALIASES.get(phrase, phrase)
        terms = list(dict.fromkeys(re.findall(r"\w+", phrase)))[:12]
        if not terms:
            return []
        words = [re.compile(rf"\b{re.escape(term)}s?\b") for term in terms]
        exact_phrase = re.compile(rf"(?<!\w){re.escape(phrase)}(?!\w)")
        results = []
        for guide in self.available():
            if guide.group == "Earlier notes":
                continue
            try:
                document = self.read(guide.slug)
            except GuideUnavailable:
                continue
            meta = f"{guide.title} {guide.description} {guide.keywords}".casefold()
            matches = []
            for section in document.sections:
                heading = section.title.casefold()
                body = " ".join(section.text.casefold().split())
                heading_matches = [bool(word.search(heading)) for word in words]
                body_matches = [bool(word.search(body)) for word in words]
                if all(a or b for a, b in zip(heading_matches, body_matches)):
                    score = 4 * sum(heading_matches) + sum(body_matches)
                    score += 6 * bool(exact_phrase.search(heading)) + 2 * bool(exact_phrase.search(body))
                    matches.append((score, section))
            if matches:
                score, section = max(matches, key=lambda match: match[0])
            elif all(word.search(meta) for word in words):
                score, section = 0, document.sections[0]
            else:
                continue
            text = " ".join(section.text.split()) or guide.description
            offsets = [match.start() for word in words if (match := word.search(text.casefold()))]
            start = max(0, min(offsets, default=0) - 60)
            if start:
                start = text.rfind(" ", 0, start) + 1
            excerpt = ("…" if start else "") + text[start:start + 240] + ("…" if len(text) > start + 240 else "")
            score += 2 * sum(bool(word.search(guide.title.casefold())) for word in words)
            results.append(SearchHit(guide, excerpt, section, score))
        return sorted(results, key=lambda result: result.score, reverse=True)

    def related(self, guide: Guide) -> list[Guide]:
        available = self.available()
        same_group = [g for g in available if g.slug != guide.slug and g.group == guide.group]
        return (same_group + [g for g in available if g.slug in {"getting-more", "troubleshooting"} and g not in same_group and g.slug != guide.slug])[:3]
