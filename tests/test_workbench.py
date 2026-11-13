"""Boundaries that matter: once-only dispatch, recovery and lossless restore."""

import json
import sqlite3
from threading import Event

import pytest
from pydantic import ValidationError

from lib.workbench.everyday_recipes import EVERYDAY_RECIPES
from lib.workbench.models import Backup, Recipe, Result, Run, Step
from lib.workbench.parent_insight_recipes import PARENT_INSIGHT_RECIPES
from lib.workbench.recipes import RECIPES, worked_example
from lib.workbench.runner import Runner, render_prompt, validate_recipe
from lib.workbench.store import Conflict, Store
from lib.workbench.teacher_insight_recipes import TEACHER_INSIGHT_RECIPES
from lib.workbench.teacher_recipes import TEACHER_RECIPES


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
    assert set(RECIPES) == {
        "explain", "connect", "decide", "write", "untangle", "learn", "family-game", "memory-comic", "home-invention",
        *EVERYDAY_RECIPES,
        *TEACHER_RECIPES,
        *PARENT_INSIGHT_RECIPES,
        *TEACHER_INSIGHT_RECIPES,
    }
    assert len(PARENT_INSIGHT_RECIPES) == len(TEACHER_INSIGHT_RECIPES) == 10
    assert len(RECIPES) == 9 + len(EVERYDAY_RECIPES) + len(TEACHER_RECIPES) + 20
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


def test_pause_during_prompt_render_prevents_next_dispatch(store, recipe, monkeypatch):
    run = run_for(store, recipe, review_each=False)
    calls = []
    rendering, release = Event(), Event()

    def delayed_render(prompt, current):
        if current.results:
            rendering.set()
            assert release.wait(3)
        return render_prompt(prompt, current)

    def call(_model, prompt):
        calls.append(prompt)
        return "answer", None

    monkeypatch.setattr("lib.workbench.runner.render_prompt", delayed_render)
    runner = runner_for(store, call)
    try:
        work = runner.start(run.id, run.revision)
        assert rendering.wait(3)
        active = store.get_run(run.id)
        assert len(active.results) == len(calls) == 1 and active.active_attempt_id is None
        with pytest.raises(Conflict, match="earlier execution"):
            runner.pause(run.id, "0" * 32)
        runner.pause(run.id, active.execution_id)
        release.set()
        work.result(timeout=3)
        stopped = store.get_run(run.id)
        assert len(calls) == 1 and stopped.state == "paused"
        assert stopped.active_attempt_id is stopped.execution_id is None
    finally:
        release.set()
        runner.close()


def test_failed_checkpoint_can_be_saved_without_calling_provider_again(store, recipe, monkeypatch):
    run = run_for(store, recipe, review_each=False)
    calls = []

    def call(_model, prompt):
        calls.append(prompt)
        return "answer already received", None

    def locked(*_args, **_kwargs):
        raise sqlite3.OperationalError("locked")

    runner = runner_for(store, call)
    try:
        with monkeypatch.context() as patch:
            patch.setattr(store, "finish_step", locked)
            runner.start(run.id, run.revision).result(timeout=3)
            assert runner.pending_save(run.id)
            assert store.read_pending_checkpoint().result.output == "answer already received"
            with pytest.raises(sqlite3.OperationalError):
                runner.retry_save(run.id)
            with pytest.raises(Conflict, match="waiting to save"):
                runner.start(run.id, store.get_run(run.id).revision)
        saved = runner.retry_save(run.id)
        assert saved.state == "paused" and len(calls) == 1
        assert saved.results[0].output == "answer already received"
        assert not runner.pending_save(run.id) and not store.pending_path.exists()
        assert saved.total_tokens is None and not saved.usage_complete
    finally:
        runner.close()


def test_restart_recovers_a_pending_answer_without_provider_calls(store, recipe, monkeypatch):
    run = run_for(store, recipe, review_each=False)
    original = runner_for(store, lambda *_: ("preserve this response", {"total_tokens": 12}))

    def locked(*_args, **_kwargs):
        raise sqlite3.OperationalError("locked")

    with monkeypatch.context() as patch:
        patch.setattr(store, "finish_step", locked)
        try:
            original.start(run.id, run.revision).result(timeout=3)
            assert original.pending_save(run.id)
        finally:
            original.close()
    assert store.pending_path.is_file()
    reopened = runner_for(store, lambda *_: pytest.fail("Recovery called a provider"))
    try:
        reopened.open()
        saved = store.get_run(run.id)
        assert saved.state == "paused"
        assert saved.results[0].output == "preserve this response"
        assert saved.results[0].attempt_id
        assert saved.total_tokens == 12 and saved.usage_complete
        assert not reopened.pending_save(run.id) and not store.pending_path.exists()
    finally:
        reopened.close()


def test_truncated_completion_is_preserved_and_stops_for_review(store, recipe):
    from lib.core.llm_client import Completion

    run = run_for(store, recipe, review_each=False)
    calls = []

    def call(_model, prompt):
        calls.append(prompt)
        return Completion(
            text="A partial answer", finish_reason="length", response_id="response-1",
            response_model="actual/model", usage={"total_tokens": 3},
        )

    runner = runner_for(store, call)
    try:
        runner.start(run.id, run.revision).result(timeout=3)
        saved = store.get_run(run.id)
        assert saved.state == "paused" and len(calls) == 1
        assert "token limit" in saved.review_notice
        assert saved.results[0].output == "A partial answer"
        assert saved.results[0].response_id == "response-1"
        assert saved.results[0].response_model == "actual/model"
        assert saved.results[0].reported_tokens == 3
    finally:
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
    collision = next(item for item in other.runs() if item.id != run.id)
    other.mutate(collision.id, lambda current: setattr(current, "topic", "Edited imported copy"))
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


def test_restore_rejects_nonfinite_duration_unversioned_data_and_unsafe_dates(store):
    sample = worked_example()
    raw = Backup(runs=[sample]).model_dump_json()
    for invalid in (
        raw.replace('"seconds":0.0', '"seconds":1e309', 1),
        raw.replace(sample.updated_at, "0001-01-01T00:00:00+00:00"),
        raw.replace('"version":1', '"version":true', 1),
        "{}",
    ):
        with pytest.raises(ValueError):
            store.restore(invalid.encode())
        assert not store.runs()


def test_legacy_results_keep_unknown_usage_and_round_trip(store, recipe):
    old_result = {
        "prompt": "Prior prompt", "output": "Prior answer", "seconds": 1.5,
        "prompt_tokens": 0, "completion_tokens": 0, "edited": False, "original_output": None,
    }
    old_run = run_for(store, recipe, state="paused", results=[Result.model_validate(old_result)])
    raw = Backup(runs=[old_run]).model_dump()
    archived = raw["runs"][0]
    for field in ("practice_case", "review_notice", "execution_id", "active_attempt_id",
                  "resume_note", "archived", "parent_run_id", "forked_after_step"):
        archived.pop(field)
    archived["results"] = [old_result]
    assert store.restore(json.dumps(raw).encode()) == (0, 0)
    saved = store.get_run(old_run.id)
    assert saved.results[0].output == "Prior answer"
    assert saved.total_tokens is None and not saved.usage_complete


def test_run_summaries_search_and_paginate_and_active_run_gets_priority(store, recipe):
    active = run_for(store, recipe, state="running", results=[Result(prompt="sent", output="answer")])
    newer = store.create_run(Run(recipe=recipe, topic="Straße example"))
    assert store.resume_run().id == active.id
    assert store.run_summaries(limit=1)[0].id == newer.id
    assert store.run_summaries(limit=1, offset=1)[0].saved_steps == 1
    assert store.run_summaries("STRASSE")[0].title == recipe.title
    assert store.run_summaries("completed") == []


def test_resume_note_and_archive_survive_backup_and_restore(store, recipe, tmp_path):
    run = run_for(store, recipe)
    saved = store.set_resume_note(run.id, "  Check the assumptions next.  ", run.revision)
    assert store.resume_run().resume_note == "Check the assumptions next."
    with pytest.raises(Conflict):
        store.set_archived(run.id, True, run.revision)
    archived = store.set_archived(run.id, True, saved.revision)
    assert store.resume_run() is None and not store.run_summaries()
    assert store.run_summaries(archived=True)[0].id == run.id
    with pytest.raises(Conflict, match="archive"):
        store.claim(run.id, archived.revision)
    destination = Store(tmp_path / "restored")
    assert destination.restore(store.archive()) == (0, 1)
    restored = destination.get_run(run.id)
    assert restored.archived and restored.resume_note == saved.resume_note
    destination.set_archived(restored.id, False, restored.revision)
    assert destination.resume_run().id == run.id


def test_checkpoint_branch_preserves_source_and_counts_only_new_usage(store, recipe):
    source = run_for(store, recipe, state="completed", results=[
        Result(prompt="Find", output="Historical first answer", total_tokens=15),
        Result(prompt="Use", output="Historical second answer", total_tokens=20),
    ])
    with pytest.raises(ValueError, match="before the end"):
        store.fork_run(source.id, 2, source.revision)
    with pytest.raises(Conflict):
        store.fork_run(source.id, 1, source.revision + 1)
    branch = store.fork_run(source.id, 1, source.revision)
    assert branch.id != source.id and branch.parent_run_id == source.id
    assert branch.forked_after_step == 1 and branch.state == "paused"
    assert branch.total_tokens is None and len(branch.results) == 1
    prompts = []
    runner = runner_for(store, lambda _, prompt: (prompts.append(prompt) or "New answer", {"total_tokens": 8}))
    try:
        edited = runner.edit_last(branch.id, "Corrected first answer", branch.revision)
        runner.start(branch.id, edited.revision).result(timeout=3)
        completed = store.get_run(branch.id)
        assert completed.state == "completed" and completed.total_tokens == 8
        assert "Corrected first answer" in prompts[0]
        assert store.get_run(source.id) == source
    finally:
        runner.close()


def test_default_provider_settings_snapshot_omits_headers(store, recipe, monkeypatch):
    from lib.core import llm_client

    monkeypatch.setattr(llm_client, "request_completion", lambda *_: llm_client.Completion("Answer"))
    monkeypatch.setattr(llm_client, "get_prompt_settings", lambda: {
        "max_tokens": 512, "temperature": 0.25, "timeout": 10, "headers": {"Private": "exclude-me"},
    })
    run = run_for(store, recipe)
    runner = Runner(store, model_factory=lambda: (None, ("test/model",)))
    try:
        runner.start(run.id, run.revision).result(timeout=3)
        saved = store.get_run(run.id)
        assert saved.results[0].model_settings.model_dump() == {
            "max_tokens": 512, "temperature": 0.25, "timeout_seconds": 10.0,
        }
        assert "exclude-me" not in saved.model_dump_json()
    finally:
        runner.close()


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


def test_recovery_preserves_unreadable_run_and_releases_its_claim(tmp_path):
    store = Store(tmp_path)
    original = '{"state":"running","results":[{"seconds":null}]}'
    with store.connection() as db:
        db.execute("INSERT INTO runs VALUES (?, ?, ?, ?)", ("a" * 32, "running", "", original))
    assert store.recover() == 1
    assert store.running_ids() == []
    with store.connection() as db:
        assert db.execute("SELECT payload FROM runs").fetchone()[0] == original
