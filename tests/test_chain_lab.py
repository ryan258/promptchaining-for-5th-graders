"""Offline Chain Lab route coverage with a temporary workspace."""

from html import escape

import pytest
from fastapi.testclient import TestClient

from lib.core import llm_client
from lib.workbench.chain_lab import plan_prompt
from lib.workbench.chain_lab_missions import CHAIN_LAB_MISSIONS
from lib.workbench.kid_insight_missions import KID_INSIGHT_MISSIONS
from lib.workbench.runner import render_prompt
from lib.workbench.store import Store
from server import workbench
from server.main import app


GOAL = "Make a route for the open house."
CLUES = "Use a blue ribbon and keep the doors clear."
PLAN = {
    "topic": GOAL,
    "context": CLUES,
    "step_name": ["Route planner", "Sign writer", "Put it together", "Check the plan", ""],
    "step_prompt": [
        "Make a route for [Goal]\nClues: [Clues]",
        "Write a one-line sign for [Goal]",
        "Use this route: [Answer 1]\nUse this sign: [Answer 2]",
        "Check this plan: [Answer 3]\nCheck it against these clues: [Clues]",
        "",
    ],
}


@pytest.fixture
def client(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_MODELS", "test/model")
    monkeypatch.setattr(workbench, "load_dotenv", lambda *_: None)
    monkeypatch.setattr(llm_client, "load_dotenv", lambda *_: None)
    with TestClient(app) as session:
        runner = workbench.get_runner()
        runner.model_factory = lambda: pytest.fail("Chain Lab tried to configure a provider")
        runner.call = lambda *_: pytest.fail("Chain Lab tried to request a model answer")
        yield session


def open_lab(client, mission=""):
    opened = client.post("/studio/lab", data={"mission": mission}, follow_redirects=False)
    assert opened.status_code == 303
    run_id = opened.headers["location"].rstrip("/").rsplit("/", 1)[-1]
    return workbench.get_store().get_run(run_id)


def test_chain_lab_prepares_a_separate_openrouter_free_run(client, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    draft = open_lab(client, "ice-cup-test")
    path = f"/studio/lab/{draft.id}/plan"
    assert "Prepare free AI run" in client.get(f"/studio/runs/{draft.id}").text

    prepared = client.post(path, data={
        **PLAN, "revision": draft.revision, "action": "free-ai", "model": "test/model",
    }, follow_redirects=False)
    assert prepared.status_code == 303
    location = prepared.headers["location"]
    assert location.startswith("/studio/runs/") and location != f"/studio/runs/{draft.id}"
    store = workbench.get_store()
    saved_lab = store.get_run(draft.id)
    live = store.get_run(location.rsplit("/", 1)[-1])
    assert saved_lab.mode == "lab" and saved_lab.state == "ready" and not saved_lab.results
    assert saved_lab.topic == GOAL and saved_lab.context == CLUES
    assert live.mode == "live" and live.model == "openrouter/free"
    assert live.state == "ready" and live.review_each and not live.results
    assert live.recipe == saved_lab.recipe and live.topic == saved_lab.topic and live.context == saved_lab.context
    assert len(store.runs()) == 2

    preview = client.get(location)
    assert preview.status_code == 200
    assert escape(render_prompt(live.recipe.steps[0].prompt, live)) in preview.text

    stale = client.post(path, data={**PLAN, "revision": draft.revision, "action": "free-ai"})
    assert stale.status_code == 409
    assert len(store.runs()) == 2


def test_chain_lab_rejects_openrouter_free_without_a_key(client):
    draft = open_lab(client)
    assert "Prepare free AI run" not in client.get(f"/studio/runs/{draft.id}").text
    rejected = client.post(f"/studio/lab/{draft.id}/plan", data={
        **PLAN, "revision": draft.revision, "action": "free-ai",
    })
    assert rejected.status_code == 400
    assert "Use this route: [Answer 1]" in rejected.text
    assert workbench.get_store().runs() == [draft]


def test_lab_runs_a_student_plan_with_two_independent_answers(client, tmp_path):
    chooser = client.get("/studio/lab")
    assert chooser.status_code == 200
    _, anchor, discovery_section = chooser.text.partition('id="insight-missions"')
    assert anchor and len(KID_INSIGHT_MISSIONS) == 10
    for slug in KID_INSIGHT_MISSIONS:
        assert f'name="mission" value="{slug}"' in discovery_section
    store = workbench.get_store()
    assert not store.runs()
    draft = open_lab(client)
    lab = f"/studio/lab/{draft.id}"
    saved_run = f"/studio/runs/{draft.id}"
    assert draft.mode == "lab" and draft.state == "ready" and not draft.results
    assert client.get(saved_run).status_code == 200

    draft_saved = client.post(f"{lab}/plan", data={**PLAN, "revision": draft.revision, "action": "save"})
    assert draft_saved.status_code == 200
    assert "Your plan is saved" in draft_saved.text
    draft = store.get_run(draft.id)
    assert draft.state == "ready" and draft.topic == GOAL and not draft.results
    assert "Use this route: [Answer 1]" in client.get(saved_run).text

    planned = client.post(f"{lab}/plan", data={**PLAN, "revision": draft.revision, "action": "play"})
    assert planned.status_code == 200
    assert escape(CLUES) in planned.text
    assert client.get(f"{saved_run}/export?format=final").status_code == 409

    route = "Follow the blue ribbon <by the wall>. Keep [Answer 2] and {{topic}} as written."
    sign = "Open house this way."
    combined = "Follow the blue ribbon past the sign to the open house."
    checked = "Keep the ribbon and sign along the wall so the doors stay clear."
    expected_prompts = [
        f"Make a route for {GOAL}\nClues: {CLUES}",
        f"Write a one-line sign for {GOAL}",
        f"Use this route: {route}\nUse this sign: {sign}",
        f"Check this plan: {combined}\nCheck it against these clues: {CLUES}",
    ]
    for index, answer in enumerate((route, sign, combined, checked)):
        active = store.get_run(draft.id)
        assert active.state == "paused" and len(active.results) == index
        resumed = client.get(saved_run)
        assert resumed.status_code == 200
        if index == 2:
            assert escape(route) in resumed.text and sign in resumed.text
        response = client.post(f"{lab}/answer", data={"revision": active.revision, "answer": answer})
        assert response.status_code == 200
        checkpoint = store.get_run(draft.id).results[index]
        assert checkpoint.output == answer
        assert checkpoint.prompt == expected_prompts[index]

    original = store.get_run(draft.id)
    assert original.state == "completed"
    assert saved_run in client.get("/studio/library").text
    for export_format in ("markdown", "final", "trace"):
        export = client.get(f"{saved_run}/export", params={"format": export_format})
        assert export.status_code == 200
        assert checked in export.text and "human" in export.text.casefold()
        if export_format == "trace":
            assert expected_prompts[2] in export.text
    backup = client.get(f"{saved_run}/export?format=json")
    restored = Store(tmp_path / "restored")
    assert restored.restore(backup.content) == (0, 1)
    assert restored.get_run(draft.id) == original

    remixed = client.post(f"{lab}/remix", data={"revision": original.revision}, follow_redirects=False)
    assert remixed.status_code == 303
    remix_path = remixed.headers["location"]
    remix_id = remix_path.rstrip("/").rsplit("/", 1)[-1]
    copy = store.get_run(remix_id)
    assert copy.id != original.id and copy.mode == "lab" and copy.state == "ready"
    assert copy.parent_run_id == original.id and copy.forked_after_step == 0
    assert not copy.results
    assert copy.recipe.steps == original.recipe.steps
    assert copy.topic == original.topic and copy.context == original.context
    assert "[Answer 1]" in client.get(remix_path).text

    revised_plan = {
        **PLAN,
        "revision": copy.revision,
        "step_name": ["Route planner", "Write the sign"],
        "step_prompt": [PLAN["step_prompt"][0], "Turn [Answer 1] into a one-line sign."],
    }
    remix = f"/studio/lab/{copy.id}"
    remix_start = client.post(f"{remix}/plan", data=revised_plan)
    assert remix_start.status_code == 200
    assert "Reuse original answer" in remix_start.text and escape(route) in remix_start.text
    new_final = "Open house this way. Follow the blue ribbon."
    for answer in (route, new_final):
        active = store.get_run(copy.id)
        compared = client.post(f"{remix}/answer", data={"revision": active.revision, "answer": answer})
        assert compared.status_code == 200
        assert "Reuse original answer" not in compared.text
    assert checked in compared.text and new_final in compared.text
    assert store.get_run(original.id) == original


def test_lab_rejects_forward_refs_stale_forms_and_non_lab_actions(client, monkeypatch, tmp_path):
    store = workbench.get_store()
    draft = open_lab(client)
    lab = f"/studio/lab/{draft.id}"
    saved_run = f"/studio/runs/{draft.id}"

    prompts = list(PLAN["step_prompt"])
    prompts[0] = "Use [Answer 2] before it exists."
    rejected_plan = client.post(f"{lab}/plan", data={**PLAN, "step_prompt": prompts, "revision": draft.revision})
    assert rejected_plan.status_code == 400
    assert "Use [Answer 2] before it exists." in rejected_plan.text
    assert store.get_run(draft.id) == draft

    valid_plan = {**PLAN, "revision": draft.revision}
    assert client.post(f"{lab}/plan", data=valid_plan).status_code == 200
    active = store.get_run(draft.id)
    assert client.post(f"{lab}/plan", data=valid_plan).status_code == 409
    assert store.get_run(draft.id) == active

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    continue_run = client.post(f"{saved_run}/continue", data={"revision": active.revision})
    assert continue_run.status_code == 409
    assert store.get_run(draft.id) == active

    first = {"revision": active.revision, "answer": "Follow the blue ribbon."}
    assert client.post(f"{lab}/answer", data=first).status_code == 200
    paused = store.get_run(draft.id)
    assert client.post(f"{lab}/answer", data={**first, "answer": "This belongs to the old prompt."}).status_code == 409
    edit = client.post(f"{saved_run}/edit", data={"revision": paused.revision, "output": "Unrecorded change"})
    assert edit.status_code == 409
    assert store.get_run(draft.id) == paused
    backup = client.get(f"{saved_run}/export?format=json")
    restored = Store(tmp_path / "restored")
    assert restored.restore(backup.content) == (0, 1)
    assert restored.get_run(draft.id) == paused

    organize = f"{saved_run}/organize"
    assert client.post(organize, data={"revision": paused.revision, "action": "archive"}).status_code == 200
    archived = store.get_run(draft.id)
    assert archived.archived
    assert client.post(f"{lab}/answer", data={"revision": archived.revision, "answer": "A sign."}).status_code == 409
    assert store.get_run(draft.id) == archived
    assert client.post(organize, data={"revision": archived.revision, "action": "unarchive"}).status_code == 200
    resumed = store.get_run(draft.id)
    assert not resumed.archived and resumed.results == paused.results


@pytest.mark.parametrize("mission", list(CHAIN_LAB_MISSIONS))
def test_mission_starter_plan_is_playable(client, mission):
    draft = open_lab(client, mission)
    expected = CHAIN_LAB_MISSIONS[mission]
    assert draft.recipe == expected.recipe and draft.context == expected.context
    assert draft.topic == expected.topic
    response = client.post(f"/studio/lab/{draft.id}/plan", data={
        "revision": draft.revision,
        "topic": draft.topic,
        "context": draft.context,
        "step_name": [step.name for step in draft.recipe.steps],
        "step_prompt": [plan_prompt(step.prompt, index) for index, step in enumerate(draft.recipe.steps)],
    })
    assert response.status_code == 200
    planned = workbench.get_store().get_run(draft.id)
    assert planned.state == "paused" and planned.recipe == expected.recipe
    for index in range(len(planned.recipe.steps)):
        response = client.post(f"/studio/lab/{draft.id}/answer", data={
            "revision": planned.revision, "answer": f"Human answer {index + 1}.",
        })
        assert response.status_code == 200
        planned = workbench.get_store().get_run(draft.id)
    assert planned.state == "completed"
    assert planned.results[-2].output in planned.results[-1].prompt
