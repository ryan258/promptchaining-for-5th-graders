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
    Guide("building-chains", "docs/CHAIN-BUILDING.md", "Build your own chains", "Connect prompts and answers, with a complete three-step recipe.", "Make it yours", "placeholders variables output custom JSON"),
    Guide("accessibility", "docs/DAILY-USE-AND-ACCESSIBILITY.md", "Less typing, easier return", "Use dictation, shortcuts, saved methods, and small sessions.", "Make it yours", "keyboard voice aliases drafts resume"),
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
    Guide("legacy-demos", "docs/DEMOS.md", "Earlier framework demos", "Older walkthroughs; inspect a script before making provider calls.", "Earlier notes"),
    Guide("ideas", "docs/IDEAS.md", "Earlier ideas", "The historical inventory of project ideas and proposals.", "Earlier notes"),
    Guide("changelog", "docs/CHANGELOG.md", "Historical changelog", "Earlier development changes.", "Earlier notes"),
    Guide("release-notes", "docs/WHATS_NEW.md", "Earlier release notes", "Notes describing previous versions of the framework.", "Earlier notes"),
)


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
        if candidate.resolve() != candidate or not candidate.is_file():
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
                    return urlunsplit(("", "", url.path or "/", url.query, url.fragment)), False
                return target, True
            if url.netloc:
                return None, False
            if not url.path:
                return ("#" + url.fragment) if url.fragment else "#main", False
            if url.path == "/" or url.path.startswith("/studio/"):
                return target, False
            path = (self.root / Path(current.source).parent / unquote(url.path)).resolve()
            guide = self.sources.get(path)
            if guide is None:
                return None, False
            self._path(guide)
            return guide.href + ("#" + url.fragment if url.fragment else ""), False
        except (ValueError, OSError):
            return None, False

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
        used_ids: dict[str, int] = {}

        for index, token in enumerate(tokens):
            if token.type == "heading_open" and index + 1 < len(tokens):
                heading = self._plain(tokens[index + 1])
                base = re.sub(r"\s+", "-", "".join(ch for ch in heading.casefold() if ch.isalnum() or ch in " _-").strip()) or "section"
                count = used_ids.get(base, 0)
                used_ids[base] = count + 1
                anchor = base if count == 0 else f"{base}-{count}"
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
        terms = list(dict.fromkeys(re.findall(r"\w+", query.casefold())))[:12]
        if not terms:
            return []
        results = []
        for guide in self.available():
            try:
                document = self.read(guide.slug)
            except GuideUnavailable:
                continue
            meta = f"{guide.title} {guide.description} {guide.keywords}".casefold()
            corpus = meta + " " + " ".join(section.text.casefold() for section in document.sections)
            if not all(term in corpus for term in terms):
                continue
            section = max(document.sections, key=lambda s: sum(3 * (term in s.title.casefold()) + (term in s.text.casefold()) for term in terms))
            text = " ".join(section.text.split()) or guide.description
            offsets = [text.casefold().find(term) for term in terms if term in text.casefold()]
            start = max(0, min(offsets, default=0) - 60)
            if start:
                start = text.rfind(" ", 0, start) + 1
            excerpt = ("…" if start else "") + text[start:start + 240] + ("…" if len(text) > start + 240 else "")
            score = sum(8 * (term in guide.title.casefold()) + 3 * (term in meta) for term in terms)
            score -= 8 if guide.group == "Earlier notes" else 0
            results.append(SearchHit(guide, excerpt, section, score))
        return sorted(results, key=lambda result: result.score, reverse=True)

    def related(self, guide: Guide) -> list[Guide]:
        available = self.available()
        same_group = [g for g in available if g.slug != guide.slug and g.group == guide.group]
        return (same_group + [g for g in available if g.slug in {"getting-more", "troubleshooting"} and g not in same_group and g.slug != guide.slug])[:3]
