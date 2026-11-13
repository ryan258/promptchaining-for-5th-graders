"""Offline route acceptance; all storage and model calls are isolated."""

import json
import re

import pytest
from fastapi.testclient import TestClient
from markupsafe import escape

from lib.core import llm_client
from lib.workbench.everyday_recipes import EVERYDAY_RECIPE_EXAMPLES
from lib.workbench.models import Backup, Result
from lib.workbench.parent_insight_recipes import PARENT_INSIGHT_RECIPES
from lib.workbench.recipes import PARENT_RECIPE_EXAMPLES, RECIPES, RECIPE_EXAMPLES, RECIPE_INPUT_HINTS, worked_example
from lib.workbench.runner import render_prompt
from lib.workbench.teacher_insight_recipes import TEACHER_INSIGHT_RECIPES
from lib.workbench.teacher_recipes import TEACHER_RECIPE_EXAMPLES
from server import workbench
from server.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODELS", "test/model")
    monkeypatch.setattr(workbench, "load_dotenv", lambda *_: None)
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    with TestClient(app) as session:
        runner = workbench.get_runner()
        runner.model_factory = lambda: (object(), ("test/model",))
        runner.call = lambda *_: pytest.fail("A page read, preparation or restore made a model request")
        yield session


def recipe_form(action="save", *, spec=None, **extra):
    spec = spec or RECIPES["connect"]
    return {"title": spec.title, "description": spec.description, "audience": spec.audience,
            "topic": "A topic I dictated", "context": "A note I want to keep", "model": "test/model",
            "step_name": [s.name for s in spec.steps], "step_purpose": [s.purpose for s in spec.steps],
            "step_prompt": [s.prompt for s in spec.steps], "action": action, "review_each": "on", **extra}


def test_workbench_pages_render_without_remote_ui_dependencies(client):
    for path, marker in [("/", "Try a classroom challenge"), ("/studio/recipes", "Pick a recipe"),
                         ("/studio/new", "Give your chain a job"), ("/studio/new?recipe=blank", "My new chain"),
                         ("/studio/library", "A place to come back to"), ("/studio/learn", "What is a prompt chain?"),
                         ("/studio/advanced", "A few deeper tools")]:
        response = client.get(path)
        assert response.status_code == 200, path
        assert marker in response.text
        assert "https://unpkg.com" not in response.text
        assert "fonts.googleapis.com" not in response.text
        assert 'href="#main"' in response.text
    asset = client.get("/static/vendor/htmx-1.9.12.min.js")
    assert asset.status_code == 200 and len(asset.content) > 40000


def test_home_shows_each_audience_its_chains_before_the_prompt_example(client):
    response = client.get("/")
    assert response.status_code == 200
    _, chooser, after_chooser = response.text.partition('id="choose-your-path"')
    assert chooser
    paths, example, after_example = after_chooser.partition('id="prompt-example-title"')
    assert example and "A tiny kite and a cracked eggshell." in after_example

    cards = re.split(r"<h[23]\b[^>]*>\s*(Kids|Parents and caregivers|Teachers)\s*</h[23]>", paths)[1:]
    assert cards[::2] == ["Kids", "Parents and caregivers", "Teachers"]
    destinations = [
        ("/studio/practice", "/studio/lab", "/studio/lab#insight-missions", "/studio/practice#make-at-home"),
        ("/studio/recipes#for-parents", "/studio/recipes#parent-insights",
         *(f"/studio/new?recipe={key}" for key in EVERYDAY_RECIPE_EXAMPLES)),
        ("/studio/recipes#for-teachers", "/studio/recipes#teacher-insights",
         *(f"/studio/new?recipe={key}" for key in TEACHER_RECIPE_EXAMPLES)),
    ]
    for group, card, links in zip(("kids", "parents", "teachers"), cards[1::2], destinations):
        assert f'href="#home-{group}"' in paths
        assert f'id="home-{group}" tabindex="-1"' in paths
        for link in links:
            assert f'href="{link}"' in card


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


@pytest.mark.parametrize("configured, expected", [
    ("", ["openrouter/free"]),
    ("test/first,test/second", ["test/first", "test/second", "openrouter/free"]),
    ("test/first,openrouter/free,test/second", ["test/first", "openrouter/free", "test/second"]),
])
def test_openrouter_free_can_prepare_a_recipe(client, monkeypatch, configured, expected):
    monkeypatch.setenv("OPENROUTER_MODELS", configured)
    monkeypatch.delenv("DEFAULT_MODEL", raising=False)
    workbench.get_runner().model_factory = lambda: pytest.fail("Preparing a recipe constructed a provider client")
    slug = "lesson-plan"
    page = client.get(f"/studio/new?recipe={slug}")
    assert page.status_code == 200
    model_choices = page.text.split('id="chain-model"', 1)[1].split("</select>", 1)[0]
    assert re.findall(r'<option\s+value="([^"]+)"', model_choices) == expected
    assert "OpenRouter Free (openrouter/free)" in model_choices
    assert 'data-prepare-run disabled' not in page.text

    prepared = client.post("/studio/prepare", data=recipe_form(
        "run", spec=RECIPES[slug], source=slug, model="openrouter/free",
    ))
    assert prepared.status_code == 200
    run, = workbench.get_store().runs()
    assert run.model == "openrouter/free"
    assert run.state == "ready" and run.review_each and not run.results
    assert escape(render_prompt(run.recipe.steps[0].prompt, run)) in prepared.text


def test_openrouter_free_requires_a_key_to_prepare_a_recipe(client, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY")
    monkeypatch.setenv("OPENROUTER_MODELS", "openrouter/free")
    page = client.get("/studio/new?recipe=school-inbox")
    assert page.status_code == 200
    assert 'data-prepare-run disabled' in page.text
    rejected = client.post("/studio/prepare", data=recipe_form("run", model="openrouter/free"))
    assert rejected.status_code == 400
    assert not workbench.get_store().runs()


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


@pytest.mark.parametrize("case_slug", ["decision-memo", "evidence-brief", "document-review"])
def test_practice_edit_handoff_and_exports_offline(client, monkeypatch, case_slug):
    monkeypatch.delenv("OPENROUTER_API_KEY")
    assert case_slug in client.get("/studio/practice/professional").text
    opened = client.post(f"/studio/practice/{case_slug}", follow_redirects=False)
    assert opened.status_code == 303
    path = opened.headers["location"]
    assert "Read the source packet and review rubric" in client.get(path).text
    assert client.get(f"{path}/export?format=final").status_code == 409
    for _ in range(2):
        run = workbench.get_store().get_run(path.rsplit("/", 1)[-1])
        assert client.post(f"{path}/continue", data={"revision": run.revision}, follow_redirects=False).status_code == 303
    run = workbench.get_store().get_run(run.id)
    assert run.state == "paused"
    assert len(run.results) == 2
    revision = "My source-grounded correction before the final handoff."
    edited = client.post(f"{path}/edit", data={"revision": run.revision, "output": revision})
    assert edited.status_code == 200
    assert revision in edited.text
    run = workbench.get_store().get_run(run.id)
    completed = client.post(f"{path}/continue", data={"revision": run.revision})
    assert completed.status_code == 200
    assert "Authored reference deliverable" in completed.text
    trace = client.get(f"{path}/export?format=trace")
    assert trace.status_code == 200
    assert revision in trace.text and "Original answer" in trace.text
    final = client.get(f"{path}/export?format=final")
    assert final.status_code == 200
    assert "Authored sample" in final.text
    assert revision not in final.text
    assert workbench.get_store().get_run(run.id).state == "completed"


@pytest.mark.parametrize("case_slug", ["family-game", "memory-comic", "home-invention"])
def test_take_home_projects_open_matching_editable_recipes(client, case_slug):
    home = client.get("/")
    assert 'href="/studio/practice#make-at-home"' in home.text
    recipes = client.get("/studio/recipes")
    assert 'id="make-at-home"' in recipes.text
    assert f'href="/studio/new?recipe={case_slug}"' in recipes.text

    editor = client.get(f"/studio/new?recipe={case_slug}")
    assert editor.status_code == 200
    recipe = RECIPES[case_slug]
    assert f"<h1>{escape(recipe.title)}</h1>" in editor.text
    assert f'data-topic-example="{escape(PARENT_RECIPE_EXAMPLES[case_slug][1])}"' in editor.text
    assert len(recipe.steps) == 3


@pytest.mark.parametrize("shelf_id, slug", [
    ("for-parents", "school-inbox"),
    ("for-parents", "family-week"),
    ("for-parents", "weeknight-dinner"),
    ("for-parents", "school-note"),
    ("for-teachers", "lesson-plan"),
    ("for-teachers", "adapt-activity"),
    ("for-teachers", "student-feedback"),
    ("for-teachers", "exit-ticket"),
    *(("parent-insights", slug) for slug in PARENT_INSIGHT_RECIPES),
    *(("teacher-insights", slug) for slug in TEACHER_INSIGHT_RECIPES),
])
def test_starter_recipe_opens_an_example_and_prepares_a_reviewable_chain(client, shelf_id, slug):
    recipe = RECIPES[slug]
    label, topic = RECIPE_EXAMPLES[slug]
    assert f'href="/studio/recipes#{shelf_id}"' in client.get("/").text
    catalog = client.get("/studio/recipes")
    assert catalog.status_code == 200
    assert f'id="{shelf_id}"' in catalog.text
    shelf = catalog.text.split(f'id="{shelf_id}"', 1)[1].split("</section>", 1)[0]
    recipe_link = f'href="/studio/new?recipe={slug}"'
    assert recipe_link in shelf
    assert catalog.text.count(recipe_link) == 1
    assert 'href="/studio/new?recipe=family-game"' not in shelf

    editor = client.get(f"/studio/new?recipe={slug}")
    assert editor.status_code == 200
    assert f"<h1>{escape(recipe.title)}</h1>" in editor.text
    assert f'data-topic-example="{escape(topic)}"' in editor.text
    assert str(escape(label)) in editor.text
    assert str(escape(RECIPE_INPUT_HINTS[slug])) in editor.text
    assert "Copy starter chain" in editor.text
    starter = editor.text.split("data-starter-prompt>", 1)[1].split("</pre>", 1)[0]
    assert all(escape(step.prompt) in starter for step in recipe.steps)

    prepared = client.post("/studio/prepare", data=recipe_form("run", spec=recipe, source=slug, topic=topic))
    assert prepared.status_code == 200
    store = workbench.get_store()
    run, = store.runs()
    assert run.recipe == recipe and len(run.recipe.steps) == 3
    assert run.state == "ready" and run.review_each and not run.results
    first_prompt = render_prompt(recipe.steps[0].prompt, run)
    assert topic in first_prompt
    assert escape(first_prompt) in prepared.text

    def pause_with_first_answer(saved):
        saved.results.append(Result(prompt=first_prompt, output="First pass from the test model."))
        saved.state = "paused"

    paused = store.mutate(run.id, pause_with_first_answer, run.revision)
    correction = "I checked my notes and corrected the first answer."
    edited = client.post(f"/studio/runs/{run.id}/edit", data={"revision": paused.revision, "output": correction})
    assert edited.status_code == 200
    revised = store.get_run(run.id)
    second_prompt = render_prompt(recipe.steps[1].prompt, revised)
    assert correction in second_prompt
    assert escape(second_prompt) in edited.text
    revised.results.append(Result(prompt=second_prompt, output="A reviewed plan from step two."))
    assert revised.results[-1].output in render_prompt(recipe.steps[2].prompt, revised)


@pytest.mark.parametrize("slug, notes", [
    ("school-inbox", "Fictional field trip reminder. Bring the permission slip by Wednesday."),
    ("student-feedback", 'Fictional Grade 5 excerpt. "The narrator pauses before opening the door."'),
])
def test_starter_recipe_can_prepare_from_pasted_notes_alone(client, slug, notes):
    recipe = RECIPES[slug]
    prepared = client.post("/studio/prepare", data=recipe_form(
        "run", spec=recipe, source=slug, topic="", context=notes,
    ))
    assert prepared.status_code == 200
    run, = workbench.get_store().runs()
    assert run.topic == recipe.title and run.context == notes and run.state == "ready"
    assert escape(notes) in prepared.text


@pytest.mark.parametrize("slug", ["school-inbox", "lesson-plan"])
def test_starter_recipe_copy_is_available_without_model_setup(client, monkeypatch, slug):
    monkeypatch.delenv("OPENROUTER_API_KEY")
    response = client.get(f"/studio/new?recipe={slug}")
    assert response.status_code == 200
    assert 'data-prepare-run disabled' in response.text
    assert "Copy starter chain" in response.text
    assert "one step per reply" in response.text
    assert not workbench.get_store().runs()


@pytest.mark.parametrize("case_slug", [
    "rainy-recess", "missing-mascot", "paper-bridge", "family-game", "memory-comic", "home-invention",
])
def test_classroom_challenge_shows_the_students_fix_in_the_next_prompt(client, monkeypatch, case_slug):
    from lib.workbench.classroom_cases import PARENT_CASES

    monkeypatch.delenv("OPENROUTER_API_KEY")
    chooser = client.get("/studio/practice")
    assert f'action="/studio/practice/{case_slug}"' in chooser.text
    assert 'action="/studio/practice/decision-memo"' not in chooser.text
    opened = client.post(f"/studio/practice/{case_slug}", follow_redirects=False)
    assert opened.status_code == 303
    path = opened.headers["location"]
    run_id = path.rsplit("/", 1)[-1]
    store = workbench.get_store()
    assert "Read the clues" in client.get(path).text

    first = client.post(f"{path}/continue", data={"revision": store.get_run(run_id).revision})
    assert "Read the draft" in first.text
    answer = escape(store.get_run(run_id).results[0].output)
    assert first.text.count(f'<mark class="reused-answer">{answer}</mark>') == 2
    second = client.post(f"{path}/continue", data={"revision": store.get_run(run_id).revision})
    assert "Save my fix" in second.text
    assert f'action="{path}/edit"' in second.text

    correction = "Our group checked clue B and changed the draft."
    fixed = client.post(f"{path}/edit", data={"revision": store.get_run(run_id).revision, "output": correction})
    assert "Your fix goes into the next prompt" in fixed.text
    assert correction in fixed.text
    final = client.post(f"{path}/continue", data={"revision": store.get_run(run_id).revision})
    assert "How does your fix compare?" in final.text
    assert correction in store.get_run(run_id).results[-1].prompt
    if case_slug in PARENT_CASES:
        assert 'id="make-at-home"' in chooser.text
        assert "Try it at home" in final.text
        assert str(escape(PARENT_CASES[case_slug].try_next)) in final.text
        assert f'href="/studio/new?recipe={case_slug}"' in final.text
    assert client.get(f"{path}/export?format=final").status_code == 200


@pytest.mark.parametrize("case_slug", ["missing-mascot", "paper-bridge"])
def test_older_classroom_run_keeps_answers_matching_its_clues(client, case_slug):
    from lib.workbench.classroom_cases import _FIRST_CLASSROOM_CASES
    from lib.workbench.models import Recipe, Step
    from lib.workbench.practice import new_practice

    earlier = _FIRST_CLASSROOM_CASES[case_slug]
    run = new_practice(case_slug)
    run.context = earlier.context
    run.recipe = Recipe(
        title=earlier.title,
        audience=earlier.audience,
        steps=[Step(name=name, purpose=purpose, prompt=prompt) for name, purpose, prompt in earlier.steps],
    )
    store = workbench.get_store()
    store.create_run(run)
    response = client.post(f"/studio/runs/{run.id}/continue", data={"revision": run.revision})
    assert response.status_code == 200
    assert store.get_run(run.id).results[0].output == earlier.outputs[0]


@pytest.mark.parametrize("choice_index", [0, 1], ids=["map-note", "spoken-directions"])
def test_build_the_next_prompt_uses_the_same_route_for_both_jobs(client, monkeypatch, choice_index):
    from lib.workbench.classroom_cases import CHAIN_BUILDING_CASES

    monkeypatch.delenv("OPENROUTER_API_KEY")
    slug = "dragon-library"
    case = CHAIN_BUILDING_CASES[slug]
    choice, other = case.choices[choice_index], case.choices[1 - choice_index]
    assert 'href="/studio/practice#build-a-chain"' in client.get("/").text
    chooser = client.get("/studio/practice").text
    assert 'id="build-a-chain"' in chooser
    assert f'action="/studio/practice/{slug}"' in chooser
    path = client.post(f"/studio/practice/{slug}", follow_redirects=False).headers["location"]
    run_id = path.rsplit("/", 1)[-1]
    store = workbench.get_store()

    run = store.get_run(run_id)
    first = client.post(f"{path}/continue", data={"revision": run.revision})
    assert first.status_code == 200
    run = store.get_run(run_id)
    early_edit = client.post(f"{path}/edit", data={"revision": run.revision, "output": choice.instruction})
    assert early_edit.status_code == 400
    assert store.get_run(run_id).revision == run.revision

    page = client.post(f"{path}/continue", data={"revision": run.revision})
    assert page.status_code == 200
    assert "Give the last prompt a job" in page.text
    assert choice.label in page.text and other.label in page.text
    run = store.get_run(run_id)
    route = run.results[0].output
    assert route in run.results[1].prompt

    early = client.post(f"{path}/continue", data={"revision": run.revision})
    assert early.status_code == 400
    assert "Pick a job for the final prompt first" in early.text
    assert store.get_run(run_id).revision == run.revision
    invalid = client.post(f"{path}/edit", data={"revision": run.revision, "output": "Take the stairs."})
    assert invalid.status_code == 400
    assert store.get_run(run_id).revision == run.revision

    assert client.post(f"{path}/edit", data={"revision": run.revision, "output": other.instruction}).status_code == 200
    stale = client.post(f"{path}/edit", data={"revision": run.revision, "output": choice.instruction})
    assert stale.status_code == 409
    run = store.get_run(run_id)
    assert run.results[1].output == other.instruction
    assert client.post(f"{path}/edit", data={"revision": run.revision, "output": choice.instruction}).status_code == 200
    resumed = client.get(path)
    assert "You built the next prompt" in resumed.text
    assert f'<mark class="reused-answer">{escape(route)}</mark>' in resumed.text
    assert f'<mark class="reused-answer">{escape(choice.instruction)}</mark>' in resumed.text

    run = store.get_run(run_id)
    final = client.post(f"{path}/continue", data={"revision": run.revision})
    assert final.status_code == 200
    assert "Same route, two answers" in final.text
    assert "We wrote both examples ahead of time" in final.text
    assert escape(choice.example) in final.text and escape(other.example) in final.text
    assert "Try a third job at home" in final.text
    run = store.get_run(run_id)
    assert run.state == "completed"
    assert route in run.results[2].prompt and choice.instruction in run.results[2].prompt
    assert other.instruction not in run.results[2].prompt
    assert run.results[2].output == choice.example
    export = client.get(f"{path}/export?format=final")
    assert choice.example in export.text and other.example not in export.text


def test_invalid_editor_keeps_submitted_values(client):
    response = client.post("/studio/prepare", data=recipe_form(
        "run", step_prompt=["{{output[-1]}}"] * 3, context="Keep this dictated context."
    ))
    assert response.status_code == 400
    assert "Keep this dictated context." in response.text
    assert "aria-invalid" in response.text and "does not exist yet" in response.text
    assert not workbench.get_store().runs()


def test_unchanged_status_does_not_swap_run_content(client):
    client.post("/studio/example")
    run = workbench.get_store().runs()[0]
    path = f"/studio/runs/{run.id}/status"
    assert client.get(path, params={"revision": run.revision}).status_code == 204
    assert client.get(path, params={"revision": run.revision + 1}).status_code == 200


def test_restore_rejects_oversized_and_multiple_file_uploads(client, monkeypatch):
    monkeypatch.setattr(workbench, "ARCHIVE_LIMIT", 32)
    oversized = client.post("/studio/restore", files={"backup_file": ("backup.zip", b"x" * 17_000)})
    multiple = client.post("/studio/restore", files=[
        ("backup_file", ("one.json", b"{}")), ("backup_file", ("two.json", b"{}")),
    ])
    assert oversized.status_code == 413
    assert multiple.status_code == 400
    assert not workbench.get_store().runs()


def test_run_note_and_archive_routes(client):
    opened = client.post("/studio/practice/decision-memo", follow_redirects=False)
    path = opened.headers["location"]
    run_id = path.rsplit("/", 1)[-1]
    store = workbench.get_store()
    run = store.get_run(run_id)
    note = "Check who owns the proposed trial."
    assert client.post(f"{path}/organize", data={"action": "note", "revision": run.revision, "note": note}).status_code == 200
    assert note in client.get("/").text
    run = store.get_run(run_id)
    assert client.post(f"{path}/organize", data={"action": "archive", "revision": run.revision}).status_code == 200
    assert path not in client.get("/studio/library").text
    assert path in client.get("/studio/library?archived=true").text
    assert client.post(f"{path}/continue", data={"revision": store.get_run(run_id).revision}).status_code == 409
    assert note in client.get(path).text


def test_fork_route_preserves_source_checkpoint_without_dispatch(client):
    from lib.workbench.models import Run

    source = worked_example()
    parent = Run(recipe=source.recipe, topic="Keep my earlier path", model="test/model",
                 state="paused", results=source.results[:2])
    workbench.get_store().create_run(parent)
    path = f"/studio/runs/{parent.id}"
    response = client.post(f"{path}/organize", data={
        "action": "fork", "step_count": 1, "revision": parent.revision,
    }, follow_redirects=False)
    assert response.status_code == 303
    child_id = response.headers["location"].rsplit("/", 1)[-1]
    child = workbench.get_store().get_run(child_id)
    assert child.parent_run_id == parent.id and len(child.results) == 1
    assert len(workbench.get_store().get_run(parent.id).results) == 2
