"""Offline route acceptance; all storage and model calls are isolated."""

import json

import pytest
from fastapi.testclient import TestClient

from lib.core import llm_client
from lib.workbench.models import Backup
from lib.workbench.recipes import RECIPES, worked_example
from server import workbench
from server.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODELS", "test/model")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    with TestClient(app) as session:
        runner = workbench.get_runner()
        runner.model_factory = lambda: (object(), ("test/model",))
        runner.call = lambda *_: pytest.fail("A page read, preparation or restore made a model request")
        yield session


def recipe_form(action="save", **extra):
    spec = RECIPES["connect"]
    return {"title": spec.title, "description": spec.description, "audience": spec.audience,
            "topic": "A topic I dictated", "context": "A note I want to keep", "model": "test/model",
            "step_name": [s.name for s in spec.steps], "step_purpose": [s.purpose for s in spec.steps],
            "step_prompt": [s.prompt for s in spec.steps], "action": action, "review_each": "on", **extra}


def test_workbench_pages_render_without_remote_ui_dependencies(client):
    for path, marker in [("/", "Big ideas."), ("/studio/recipes", "Find your next thought"),
                         ("/studio/new", "Give it a direction"), ("/studio/new?recipe=blank", "My new chain"),
                         ("/studio/library", "A place to come back to"), ("/studio/learn", "One answer becomes"),
                         ("/studio/advanced", "A few deeper tools")]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert marker in response.text
        assert "https://unpkg.com" not in response.text
        assert "fonts.googleapis.com" not in response.text
        assert 'href="#main"' in response.text
    asset = client.get("/static/vendor/htmx-1.9.12.min.js")
    assert asset.status_code == 200 and len(asset.content) > 40000


def test_no_key_still_allows_recipe_saves_and_authored_example(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY")
    page = client.get("/studio/new")
    assert 'data-prepare-run disabled' in page.text
    response = client.post("/studio/prepare", data=recipe_form(), follow_redirects=False)
    assert response.status_code == 303
    assert len(workbench.get_store().recipes()) == 1
    example = client.post("/studio/example")
    assert example.status_code == 200
    assert "authored walkthrough" in example.text
    assert "No AI requests were made" in example.text
    assert len(workbench.get_store().runs()) == 1
    client.post("/studio/example")
    assert len(workbench.get_store().runs()) == 1


def test_saved_recipe_keeps_starting_inputs_and_never_overwrites_previous_copy(client):
    first = client.post("/studio/prepare", data=recipe_form())
    assert first.status_code == 200
    assert "A topic I dictated" in first.text
    assert "A note I want to keep" in first.text
    client.post("/studio/prepare", data=recipe_form(title="A revision"))
    assert {s.recipe.title for s in workbench.get_store().recipes()} == {"Connect two ideas", "A revision"}


def test_saved_recipe_keeps_the_chosen_pace(client):
    form = recipe_form()
    del form["review_each"]
    response = client.post("/studio/prepare", data=form)
    assert response.status_code == 200
    assert 'name="review_each" checked' not in response.text
    assert not workbench.get_store().recipes()[0].review_each


def test_preparing_saves_ready_run_and_preview_but_sends_no_requests(client):
    response = client.post("/studio/prepare", data=recipe_form("run"))
    assert response.status_code == 200
    run = workbench.get_store().runs()[0]
    assert run.state == "ready" and not run.results
    assert "Preview the exact next prompt" in response.text
    assert "A topic I dictated" in response.text
    assert run.id in str(response.url)


def test_invalid_forward_reference_prevents_a_run(client):
    payload = recipe_form("run", step_prompt=["{{output[-1]}}"] * 3)
    response = client.post("/studio/prepare", data=payload)
    assert response.status_code == 400
    assert "does not exist yet" in response.text
    assert workbench.get_store().runs() == []


def test_example_trace_exports_and_restores_without_network(client):
    client.post("/studio/example")
    run = workbench.get_store().runs()[0]
    status = client.get(f"/studio/runs/{run.id}/status")
    assert status.status_code == 200
    assert "The worked example" in status.text
    assert "Prompt that produced this answer" in status.text
    markdown = client.get(f"/studio/runs/{run.id}/export")
    assert "Authored worked example" in markdown.text
    assert "attachment" in markdown.headers["content-disposition"]
    exported = client.get(f"/studio/runs/{run.id}/export?format=json")
    assert Backup.model_validate_json(exported.content).runs[0].id == run.id
    backup = client.get("/studio/backup")
    response = client.post("/studio/restore", files={"backup_file": ("backup.json", backup.content, "application/json")})
    assert response.status_code == 200 and "0 recipes and 0 runs added" in response.text


def test_html_in_output_and_imported_topic_is_escaped(client):
    run = worked_example()
    run.topic = '<img src=x onerror="alert(1)">'
    run.results[-1].output = "<script>steal()</script>"
    workbench.get_store().create_run(run)
    page = client.get(f"/studio/runs/{run.id}")
    assert '<script>steal()</script>' not in page.text
    assert "&lt;script&gt;steal()&lt;/script&gt;" in page.text
    assert '<img src=x' not in page.text


def test_invalid_restore_is_atomic_and_display_does_not_echo_payload(client):
    client.post("/studio/prepare", data=recipe_form())
    original = workbench.get_store().recipes()[0].id
    response = client.post("/studio/restore", files={"backup_file": ("bad.json", b'{"api_key":"private-value"}', "application/json")})
    assert response.status_code == 400
    assert "private-value" not in response.text
    assert [r.id for r in workbench.get_store().recipes()] == [original]


def test_cross_site_mutations_and_unknown_hosts_are_rejected(client):
    assert client.post("/studio/example", headers={"Origin": "https://other.example"}).status_code == 403
    assert client.post("/studio/example", headers={"Sec-Fetch-Site": "cross-site"}).status_code == 403
    assert client.get("/", headers={"Host": "other.example"}).status_code == 400
    assert workbench.get_store().runs() == []


def test_search_and_not_found_paths_are_recoverable(client):
    client.post("/studio/example")
    assert "Why does the Moon" in client.get("/studio/library?q=moon").text
    assert "No chains match" in client.get("/studio/library?q=absent").text
    assert client.get("/studio/new?saved=missing").status_code == 404
    assert client.get("/studio/runs/missing").status_code == 404


def test_completed_answer_saves_to_local_artifacts_and_chroma_without_replacing_old_work(client, tmp_path, monkeypatch):
    monkeypatch.setattr(workbench, "ROOT", tmp_path)
    old = tmp_path / "artifacts" / "older"
    old.mkdir(parents=True)
    (old / "keep.json").write_text('{"keep": true}')
    run = workbench.get_store().create_run(worked_example())
    response = client.post(f"/studio/runs/{run.id}/artifact")
    assert response.status_code == 200 and "Final answer saved" in response.text
    path = tmp_path / "artifacts" / f"studio_{run.id}" / "final.json"
    assert json.loads(path.read_text()) == run.results[-1].output
    assert json.loads((old / "keep.json").read_text()) == {"keep": True}
    artifact_store = workbench.ArtifactStore(str(tmp_path / "artifacts"))
    assert artifact_store.chroma_collection is not None
    mirrored = artifact_store.chroma_collection.get(ids=[f"studio_{run.id}:final"])
    assert mirrored["documents"] == [run.results[-1].output]


def test_dates_follow_personal_timezone_instead_of_utc_day(monkeypatch):
    monkeypatch.setenv("STUDIO_TIMEZONE", "America/Chicago")
    assert workbench.local_date("2026-10-25T01:00:00+00:00") == "Oct 24, 2026"
    assert workbench.local_date("not-a-date") == "Date unavailable"


def test_workspace_setting_is_loaded_before_the_store_is_cached(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setattr(workbench, "ROOT", tmp_path)
    monkeypatch.setenv("PROMPT_STUDIO_DATA", "temporary-value-for-restoration")
    monkeypatch.delenv("PROMPT_STUDIO_DATA")
    expected = tmp_path / "chosen-workspace"
    (tmp_path / ".env").write_text(f'PROMPT_STUDIO_DATA="{expected}"\n')
    try:
        assert workbench.get_store().directory == expected
    finally:
        workbench.close_workbench()
