"""Boundaries that matter: once-only dispatch, recovery and lossless restore."""

import json
from threading import Event

import pytest
from pydantic import ValidationError

from lib.workbench.models import Backup, Recipe, Result, Run, Step
from lib.workbench.recipes import RECIPES, worked_example
from lib.workbench.runner import Runner, render_prompt, validate_recipe
from lib.workbench.store import Conflict, Store


@pytest.fixture
def store(tmp_path):
    return Store(tmp_path / "workspace")


@pytest.fixture
def recipe():
    return Recipe(title="A small chain", audience="Me", steps=[
        Step(name="Find", prompt="Find the pieces of {{topic}}. {{context}}"),
        Step(name="Use", prompt="For {{audience}}, use {{output[-1]}}."),
    ])


def run_for(store, recipe, **kwargs):
    return store.create_run(Run(recipe=recipe, topic="My topic", model="test/model", **kwargs))


def runner_for(store, call):
    return Runner(store, call=call, model_factory=lambda: (object(), ("test/model",)))


def test_catalog_is_valid_and_example_never_calls_a_model(monkeypatch):
    from lib.core import llm_client
    monkeypatch.setattr(llm_client, "build_models", lambda: pytest.fail("Example called a provider"))
    assert len(RECIPES) == 6
    for recipe in RECIPES.values():
        validate_recipe(recipe)
    example = worked_example()
    assert example.mode == "example"
    assert example.state == "completed"
    assert len(example.results) == 4
    assert example.results[0].output in example.results[1].prompt
    assert example.total_tokens == 0


@pytest.mark.parametrize("prompt", ["{{output[-1]}}", "{{unknown}}", "{{output[-9]}}"])
def test_bad_references_rejected_before_dispatch(prompt):
    with pytest.raises(ValueError):
        validate_recipe(Recipe(title="Broken", steps=[Step(name="First", prompt=prompt)]))


def test_substitution_does_not_execute_placeholders_inside_user_text(recipe):
    run = Run(recipe=recipe, topic="literal {{output[-1]}}", context="literal {{audience}}")
    assert render_prompt("{{topic}} / {{context}}", run) == "literal {{output[-1]}} / literal {{audience}}"
    run.results.append(Result(prompt="first", output=json.dumps({"name": "a\\b"})))
    assert render_prompt("{{output[-1].name}}", run) == "a\\b"
    with pytest.raises(ValueError, match="no JSON field"):
        render_prompt("{{output[-1].missing}}", run)


def test_failure_checkpoints_and_explicit_retry_only_runs_the_unfinished_step(store, recipe):
    run = run_for(store, recipe, review_each=False)
    responses = iter(["first answer", RuntimeError("secret provider payload"), "final answer"])
    calls = []

    def call(_model, prompt):
        calls.append(prompt)
        result = next(responses)
        if isinstance(result, Exception):
            raise result
        return result, {"prompt_tokens": 2, "completion_tokens": 3}

    runner = runner_for(store, call)
    try:
        runner.start(run.id, run.revision).result(timeout=3)
        failed = store.get_run(run.id)
        assert failed.state == "failed"
        assert len(failed.results) == 1
        assert len(calls) == 2  # No automatic retry.
        assert "secret provider payload" not in failed.error
        runner.start(run.id, failed.revision).result(timeout=3)
        complete = store.get_run(run.id)
        assert complete.state == "completed"
        assert [r.output for r in complete.results] == ["first answer", "final answer"]
        assert len(calls) == 3 and "first answer" in calls[-1]
        assert complete.total_tokens == 10
    finally:
        runner.close()


def test_review_edit_preserves_original_and_next_step_uses_the_revision(store, recipe):
    run = run_for(store, recipe)
    sent = []

    def call(_model, prompt):
        sent.append(prompt)
        return "model answer", None

    runner = runner_for(store, call)
    try:
        runner.start(run.id, 0).result(timeout=3)
        paused = store.get_run(run.id)
        assert paused.state == "paused" and len(sent) == 1
        edited = runner.edit_last(run.id, "my correction", paused.revision)
        assert edited.results[0].original_output == "model answer"
        assert edited.results[0].edited
        with pytest.raises(Conflict):
            runner.start(run.id, paused.revision)
        runner.start(run.id, edited.revision).result(timeout=3)
        assert "my correction" in sent[-1]
        assert "model answer" not in sent[-1]
        with pytest.raises(Conflict):
            runner.edit_last(run.id, "too late", store.get_run(run.id).revision)
    finally:
        runner.close()


def test_double_submit_and_overlapping_runs_cannot_dispatch(store, recipe):
    started, finish = Event(), Event()
    count = []

    def call(_model, _prompt):
        count.append(1)
        started.set()
        assert finish.wait(3)
        return "answer", {}

    first, second = run_for(store, recipe), run_for(store, recipe)
    runner = runner_for(store, call)
    try:
        future = runner.start(first.id, 0)
        assert started.wait(1)
        with pytest.raises(Conflict):
            runner.start(first.id, 0)
        with pytest.raises(Conflict):
            runner.start(second.id, 0)
        runner.pause(first.id)
        finish.set()
        future.result(timeout=3)
        assert count == [1]
        assert store.get_run(first.id).state == "paused"
        assert store.get_run(second.id).state == "ready"
    finally:
        finish.set()
        runner.close()


def test_restart_recovers_unfinished_work_without_model_calls(store, recipe):
    run = run_for(store, recipe, state="running", results=[Result(prompt="sent", output="safe answer")])
    runner = runner_for(store, lambda *_: pytest.fail("Recovery called a provider"))
    try:
        runner.open()
        restored = store.get_run(run.id)
        assert restored.state == "interrupted"
        assert restored.results[0].output == "safe answer"
        assert "may have processed" in restored.error
    finally:
        runner.close()


def test_second_server_cannot_recover_or_own_a_live_workspace(store, recipe):
    first = runner_for(store, lambda *_: ("answer", {}))
    second = runner_for(store, lambda *_: pytest.fail("Second server called a provider"))
    try:
        first.open()
        run = run_for(store, recipe, state="running")
        with pytest.raises(Conflict, match="another server"):
            second.open()
        assert store.get_run(run.id).state == "running"
        second.close()
        assert store.get_run(run.id).state == "running"
    finally:
        first.close()
        second.close()


def test_restore_round_trip_deduplicates_and_preserves_colliding_local_work(store, recipe, tmp_path):
    saved = store.save_recipe(recipe, "keep this topic", "keep this context")
    run = store.create_run(worked_example())
    raw = store.backup().model_dump_json().encode()
    other = Store(tmp_path / "restored")
    assert other.restore(raw) == (1, 1)
    assert other.get_recipe(saved.id).topic == "keep this topic"
    assert other.get_recipe(saved.id).context == "keep this context"
    assert other.get_run(run.id).model_dump() == run.model_dump()
    assert other.restore(raw) == (0, 0)
    modified = json.loads(raw)
    modified["runs"][0]["topic"] = "Different imported topic"
    assert other.restore(json.dumps(modified).encode()) == (0, 1)
    assert other.get_run(run.id).topic == run.topic
    assert len(other.runs()) == 2
    assert other.restore(json.dumps(modified).encode()) == (0, 0)
    assert len(other.runs()) == 2


def test_restore_validates_whole_backup_before_writing(store, recipe):
    record = store.save_recipe(recipe)
    raw = store.backup().model_dump()
    raw["recipes"].append({**record.model_dump(), "id": "a" * 32})
    raw["runs"] = [{"surprise": "bad record"}]
    with pytest.raises(ValidationError):
        store.restore(json.dumps(raw).encode())
    assert [r.id for r in store.recipes()] == [record.id]
    with pytest.raises(ValueError):
        store.restore(b" " * 10_000_001)


def test_restore_running_work_becomes_interrupted_and_is_idempotent(store, recipe):
    raw = Backup(runs=[Run(recipe=recipe, topic="unfinished", model="test/model", state="running")]).model_dump_json().encode()
    assert store.restore(raw) == (0, 1)
    assert store.runs()[0].state == "interrupted"
    assert store.restore(raw) == (0, 0)


def test_saved_runs_survive_a_fresh_store_and_recipes_are_snapshots(store, recipe):
    run = run_for(store, recipe)
    recipe.title = "Changed elsewhere"
    fresh = Store(store.directory)
    assert fresh.get_run(run.id).recipe.title == "A small chain"


def test_backup_writer_refuses_to_replace_an_existing_file(tmp_path):
    from tools.studio import atomic_write
    path = tmp_path / "copy.json"
    atomic_write(path, "original")
    with pytest.raises(ValueError, match="already exists"):
        atomic_write(path, "replacement")
    assert path.read_text() == "original"
