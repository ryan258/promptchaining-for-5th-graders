"""Offline acceptance for guide discovery, safe rendering and source freshness."""

from html.parser import HTMLParser
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from markdown_it import MarkdownIt

from lib.core import llm_client
from lib.workbench.guides import GUIDES, GuideBook, GuideUnavailable
from lib.workbench.models import Recipe, Run, Step
from server import guides as guide_routes, workbench
from server.main import app

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = []
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs)


@pytest.fixture
def book(tmp_path):
    (tmp_path / "docs").mkdir()
    return GuideBook(tmp_path)


def write_guide(book, source, name="QUICKSTART.md"):
    path = book.root / "docs" / name
    path.write_text(source, encoding="utf-8")
    return path


def test_every_installed_document_has_a_safe_reader_and_working_internal_links():
    book = GuideBook(ROOT)
    assert len(book.available()) == len(GUIDES)
    documents = {guide.href: book.read(guide.slug) for guide in GUIDES}
    parser = MarkdownIt("commonmark").enable("table")
    for document in documents.values():
        for token in parser.parse(document.source):
            for child in token.children or []:
                if child.type == "link_open":
                    source_link = child.attrGet("href")
                    assert book.href(document.guide, source_link)[0] is not None, (document.guide.source, source_link)
        page = Page(document.html)
        assert len(page.ids) == len(set(page.ids)), document.guide.slug
        for link in page.links:
            target = link.get("href", "")
            assert not target.endswith(".md"), target
            if target.startswith("/studio/guides/"):
                route, _, anchor = target.partition("#")
                assert route in documents, target
                if anchor:
                    assert anchor in Page(documents[route].html).ids, target
            elif target.startswith("#"):
                assert target[1:] in {*page.ids, "main", "guide-title"}, target
        assert "img" not in page.tags


def test_markdown_tables_code_and_duplicate_section_links_render(book):
    write_guide(book, '# A useful guide\n\n## Try it\n\n| A | B |\n|---|---|\n|one|two|\n\n```text\nUse {{output[-1]}} for {{topic}}.\n```\n\n## Try it\n\nMore.\n')
    document = book.read("quick-start")
    assert document.title == "A useful guide"
    assert '<h1' not in document.html
    assert '<table>' in document.html
    assert 'tabindex="0"' in document.html
    assert 'data-copy-nearest="pre"' in document.html
    assert '{{output[-1]}}' in document.html
    assert [s.anchor for s in document.sections if s.anchor] == ["try-it", "try-it-1"]


def test_heading_ids_stay_unique_with_suffixed_titles_and_reserved_landmarks(book):
    write_guide(book, "# Start\n\n## Review\n\n## Review\n\n## Review-1\n\n## Main\n\n## Guide title\n")
    page = Page(book.read("quick-start").html)
    assert page.ids == ["review", "review-1", "review-1-1", "main-1", "guide-title-1"]


def test_raw_html_unsafe_links_and_images_never_become_executable_markup(book):
    write_guide(book, '# Unsafe input\n\n<script>steal()</script>\n\n[bad](javascript:alert(1))\n\n[private](../.env)\n\n[local](file:///private/secret)\n\n![remote](https://example.com/tracking.png)\n\n```html\n<img src=x onerror="steal()">\n```\n')
    document = book.read("quick-start")
    page = Page(document.html)
    assert "script" not in page.tags and "img" not in page.tags
    assert '&lt;script&gt;' in document.html
    assert not any(link.get("href", "").startswith(("javascript:", "file:", "../")) for link in page.links)
    assert 'onerror=' not in document.html.replace('&lt;img src=x onerror=&quot;steal()&quot;&gt;', '')


def test_cross_guide_links_stay_inside_app_and_remote_links_are_deliberate(book):
    write_guide(book, '# Start\n\n[Other](CHAIN-BUILDING.md#hand-off) [Overview](../README.md) [App](http://127.0.0.1:8000/) [External](https://example.com/reference)\n')
    write_guide(book, '# Builder\n\n## Hand off\n\nUseful.\n', "CHAIN-BUILDING.md")
    (book.root / "README.md").write_text('# Project\n')
    page = Page(book.read("quick-start").html)
    assert page.links[0]["href"] == "/studio/guides/building-chains#hand-off"
    assert page.links[1]["href"] == "/studio/guides/project-overview"
    assert page.links[2]["href"] == "/"
    assert page.links[3]["target"] == "_blank"
    assert page.links[3]["rel"] == "noopener noreferrer"


def test_loopback_rewrite_blocks_cross_host_paths_and_keeps_studio_routes(book):
    write_guide(book, "# Start\n\n[Unsafe](http://localhost//example.com/a) [Unsafe too](///studio/guides) [Guide](http://localhost/studio/guides)")
    page = Page(book.read("quick-start").html)
    assert [link["href"] for link in page.links] == ["/studio/guides"]


def test_search_finds_body_text_and_a_matching_section_without_provider_calls(book):
    write_guide(book, '# Start\n\nIntro.\n\n## Recovery\n\nThe unique albatross checkpoint is saved here.\n')
    hits = book.search("ALBATROSS checkpoint")
    assert len(hits) == 1
    assert hits[0].href == "/studio/guides/quick-start#recovery"
    assert "albatross checkpoint" in hits[0].excerpt
    assert book.search("doesnotexist") == []
    assert book.search("??") == []


def test_search_prioritizes_relevant_sections_and_keeps_earlier_notes_browsable(book):
    write_guide(book, "# Start\n\n## Daily dictation\n\nUse system dictation for text fields.\n")
    write_guide(book, "# Old demos\n\n## Dictation commands\n\nhistoricalmarker\n", "LEGACY-DEMOS.md")
    hits = book.search("voice")
    assert [hit.href for hit in hits] == ["/studio/guides/quick-start#daily-dictation"]
    assert "historicalmarker" in book.read("legacy-demos").html
    assert not book.search("historicalmarker")


def test_reader_and_search_see_updated_markdown_without_a_rebuild(book):
    path = write_guide(book, '# Start\n\nOld wording.\n')
    assert "Old wording" in book.read("quick-start").html
    path.write_text('# Start\n\nNew wording: freshmarker.\n')
    assert "New wording" in book.read("quick-start").html
    assert book.search("freshmarker")[0].guide.slug == "quick-start"


def test_only_catalogued_regular_files_can_be_read(book):
    private = book.root / ".env"
    private.write_text("PRIVATE_KEY=keep-private")
    write_guide(book, '# Valid\n')
    with pytest.raises(GuideUnavailable):
        book.read("../.env")
    path = book.root / "docs" / "QUICKSTART.md"
    path.unlink()
    path.symlink_to(private)
    with pytest.raises(GuideUnavailable):
        book.read("quick-start")
    assert book.available() == []


@pytest.mark.parametrize("body", [b"x" * 2_000_001, b"\xff\xfe"])
def test_oversized_or_non_text_guides_fail_recoverably(book, body):
    (book.root / "docs" / "QUICKSTART.md").write_bytes(body)
    with pytest.raises(GuideUnavailable):
        book.read("quick-start")


@pytest.fixture
def client(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    monkeypatch.setattr(llm_client, "build_models", lambda: pytest.fail("Guides called a model"))
    session = TestClient(app)
    yield session
    session.close()
    workbench.close_workbench()


def test_guides_are_available_without_a_key_or_workspace_reads(client, monkeypatch):
    with monkeypatch.context() as patch:
        patch.setattr(workbench, "get_store", lambda: pytest.fail("Guide reading accessed workspace data"))
        for path in ("/studio/guides", "/studio/guides?q=backup", "/studio/guides/building-chains"):
            response = client.get(path)
            assert response.status_code == 200
            assert 'href="/studio/guides"' in response.text
    response = client.get("/studio/guides/building-chains")
    assert 'aria-current="page">Guides' in response.text
    assert 'aria-label="On this page"' in response.text
    assert 'href="#understand-exactly-what-carries-forward"' in response.text
    assert '{{output[-1]}}' in response.text


def test_all_installed_guide_routes_and_downloads_work(client):
    for guide in GUIDES:
        page = client.get(guide.href)
        assert page.status_code == 200, guide.slug
        assert "class=\"guide-body\"" in page.text
        download = client.get(f"{guide.href}/download")
        assert download.status_code == 200
        assert "attachment" in download.headers["content-disposition"]
        assert download.text == (ROOT / guide.source).read_bytes().decode("utf-8")


def test_search_results_escape_input_and_jump_to_sections(client):
    response = client.get("/studio/guides", params={"q": "MAX_TOKENS"})
    assert response.status_code == 200
    page = Page(response.text)
    assert any(link.get("href", "").startswith("/studio/guides/setup#") for link in page.links)
    no_result = client.get("/studio/guides", params={"q": '<script>alert("x")</script>'})
    assert no_result.status_code == 200
    assert '<script>alert("x")</script>' not in no_result.text
    assert "Let’s try another word" in no_result.text


def test_missing_guides_have_a_searchable_recovery_page(client):
    response = client.get("/studio/guides/not-a-guide")
    assert response.status_code == 404
    assert "Let’s find what you need" in response.text
    assert 'aria-label="Search the guides"' in response.text
    assert client.get("/studio/guides/not-a-guide/download").status_code == 404


def test_guides_navigation_and_context_help_reach_existing_workflows(client):
    expected = [("/", None), ("/studio/recipes", "recipes"), ("/studio/new", "building-chains"),
                ("/studio/library", "saving-and-recovery"), ("/studio/advanced", "advanced-tools"),
                ("/studio/tools", None), ("/studio/learn", "getting-more")]
    for path, context in expected:
        page = Page(client.get(path).text)
        assert any(link.get("href") == "/studio/guides" for link in page.links), path
        if context:
            assert any(link.get("href") == f"/studio/guides/{context}" and link.get("target") == "_blank" for link in page.links), path
    run = workbench.get_store().create_run(Run(recipe=Recipe(title="Check", steps=[Step(name="Start", prompt="{{topic}}")]), topic="A question", state="failed"))
    page = Page(client.get(f"/studio/runs/{run.id}").text)
    assert any(link.get("href") == "/studio/guides/troubleshooting" and link.get("target") == "_blank" for link in page.links)


def test_doctor_reports_a_missing_markdown_runtime(monkeypatch, capsys):
    import tools.studio as cli
    find_spec = cli.importlib.util.find_spec
    monkeypatch.setattr(cli.importlib.util, "find_spec", lambda name: None if name == "markdown_it" else find_spec(name))
    assert cli.main(["doctor"]) == 1
    assert "markdown_it" in capsys.readouterr().out
