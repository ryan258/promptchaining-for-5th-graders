"""Offline regressions for the reviewed failure paths. No provider or browser use."""

import asyncio
from io import BytesIO
import json
import os
from pathlib import Path
from threading import Event
from types import SimpleNamespace
import zipfile

import httpx
import pytest
from fastapi.testclient import TestClient

from lib import advanced
from lib.core import artifact_store, chain, llm_client
from lib.core.artifact_store import ArtifactStore
from lib.core.chain import FusionChain, MinimalChainable
from lib.core.chain_composer import ChainComposer, ChainStep
from lib.core.errors import InputError
from lib.core.meta_chain_generator import MetaChainGenerator
from lib.enhancements import adversarial_chains, natural_reasoning, emergence_measurement as comparisons
from lib.workbench.models import Recipe, Result, Run, SavedRecipe, Step
from lib.workbench.store import Store
from server import main as server
from tools import cost_report, studio
from tools.ms_blog import ms_content_tools


@pytest.fixture(autouse=True)
def offline_artifacts(monkeypatch):
    monkeypatch.setattr(ArtifactStore, "_init_chroma", lambda self: None)


def test_advanced_request_keeps_server_responsive(monkeypatch):
    started, release = Event(), Event()

    def blocking_pattern(*_):
        started.set()
        if not release.wait(2):
            raise RuntimeError("The event loop could not release the worker")
        return {"status": "success"}

    monkeypatch.setattr(server, "_execute_pattern", blocking_pattern)

    async def exercise():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app), base_url="http://testserver") as client:
            task = asyncio.create_task(client.post("/patterns/five_whys", json={"topic": "test"}))
            try:
                assert await asyncio.to_thread(started.wait, 1)
                assert (await asyncio.wait_for(client.get("/patterns"), .5)).status_code == 200
            finally:
                release.set()
            assert (await task).status_code == 200

    asyncio.run(exercise())


@pytest.mark.parametrize("path,form", [("/patterns/five_whys", False), ("/ui/run-pattern", True)])
def test_provider_exception_payload_is_absent_from_response_and_logs(monkeypatch, caplog, path, form):
    def failure(*_):
        raise RuntimeError("PRIVATE_PROVIDER_PAYLOAD")
    monkeypatch.setattr(server, "_execute_pattern", failure)
    with TestClient(server.app, raise_server_exceptions=False) as client:
        # Lifespan storage is redirected by the fixture below.
        response = client.post(path, data={"pattern_name": "five_whys", "problem": "test"}) if form else client.post(path, json={"topic": "test"})
    assert "PRIVATE_PROVIDER_PAYLOAD" not in response.text + caplog.text
    assert "Check" in response.text


@pytest.fixture(autouse=True)
def isolated_workspace(tmp_path, monkeypatch):
    from server import workbench
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    yield
    workbench.close_workbench()


def test_missing_meta_setup_has_safe_recovery_fragment(monkeypatch):
    def fail():
        raise ValueError("PRIVATE_CONFIGURATION")
    monkeypatch.setattr(server, "MetaChainGenerator", fail)
    response = TestClient(server.app).post("/ui/meta-design", data={"goal": "Explain a topic"})
    assert response.status_code == 200
    assert "Something interrupted" in response.text
    assert "PRIVATE_CONFIGURATION" not in response.text


def test_failed_artifact_replacement_preserves_file_and_cache(tmp_path, monkeypatch):
    store = ArtifactStore(str(tmp_path / "artifacts"))
    store.save("topic", "answer", {"old": True})
    path = tmp_path / "artifacts/topic/answer.json"
    before = path.read_bytes()
    def fail(*_):
        raise OSError("disk write failed")
    monkeypatch.setattr(artifact_store.os, "replace", fail)
    with pytest.raises(OSError):
        store.save("topic", "answer", {"new": True})
    assert path.read_bytes() == before
    assert store.get("topic", "answer") == {"old": True}
    assert not list(path.parent.glob(".artifact-*"))


def test_bad_artifact_does_not_block_valid_work_or_get_rewritten(tmp_path):
    directory = tmp_path / "artifacts/topic"
    directory.mkdir(parents=True)
    bad = directory / "broken.json"
    bad.write_text("{incomplete")
    (directory / "good.json").write_text('{"kept": true}')
    (directory / "good.meta.json").write_text("bad metadata")
    store = ArtifactStore(str(directory.parent))
    assert store.get("topic", "good") == {"kept": True}
    assert store.load_warnings == ["topic/broken.json"]
    assert bad.read_text() == "{incomplete"
    store.save("topic", "another", "usable")


def test_interrupted_metadata_update_does_not_reuse_legacy_provenance(tmp_path, monkeypatch):
    store = ArtifactStore(str(tmp_path / "artifacts"))
    store.save("topic", "answer", "old", metadata={"model": "old model"})
    folder = tmp_path / "artifacts/topic"
    sidecar = folder / "answer.meta.json"
    sidecar.write_text('{"model":"old model"}')
    os.utime(folder / "answer.json", ns=(1_000_000_000, 1_000_000_000))
    os.utime(sidecar, ns=(2_000_000_000, 2_000_000_000))
    original = artifact_store._atomic_replace
    def replace(path, text):
        if path.endswith(".meta.json"):
            raise OSError("metadata unavailable")
        original(path, text)
    monkeypatch.setattr(artifact_store, "_atomic_replace", replace)
    store.save("topic", "answer", "new", metadata={"model": "new model"})
    fresh = ArtifactStore(str(tmp_path / "artifacts"))
    assert fresh.get("topic", "answer") == "new"
    assert fresh.get_metadata("topic", "answer") == {}


def test_parallel_fusion_preserves_each_models_artifacts(tmp_path):
    store = ArtifactStore(str(tmp_path / "artifacts"))
    result = FusionChain.run({}, ["one", "two", "three", "four"],
                             llm_callable=lambda model, _: (model, {}), prompts=["Say your name"],
                             evaluator=lambda outputs: (outputs[0], [1, 0, 0, 0]), get_model_name=str,
                             artifact_store=store, topic="comparison")
    assert len(result.all_prompt_responses) == 4
    fresh = ArtifactStore(str(tmp_path / "artifacts"))
    assert set(fresh.artifacts.values()) == {"one", "two", "three", "four"}
    assert len(fresh.artifacts) == 4


@pytest.mark.parametrize("function,kwargs", [(natural_reasoning.five_whys, {"problem": "test", "depth": 10000}),
                                           (natural_reasoning.socratic_dialogue, {"belief": "test", "depth": 0}),
                                           (adversarial_chains.red_vs_blue, {"topic": "test", "position_to_defend": "test", "rounds": 10000}),
                                           (adversarial_chains.adversarial_socratic, {"claim": "test", "depth": -1})])
def test_depth_bounds_hold_for_direct_library_calls(function, kwargs):
    with pytest.raises(InputError):
        function(**kwargs, model_info=(None, "offline"), llm_callable=lambda *_: pytest.fail("Invalid bounds dispatched"))


def test_legacy_chain_makes_one_attempt_and_does_not_retry_formatting(monkeypatch):
    calls = []
    def fail(**_):
        calls.append(1)
        raise RuntimeError("offline provider failure")
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fail)))
    monkeypatch.setattr(llm_client, "get_prompt_settings", lambda: {"max_tokens": 100, "temperature": .5, "timeout": 1, "headers": {}})
    with pytest.raises(RuntimeError):
        MinimalChainable.run({}, (client, "offline"), llm_callable=llm_client.prompt, prompts=["Return JSON"])
    assert len(calls) == 1
    sent = []
    output, _ = MinimalChainable.run({}, None, llm_callable=lambda _, text: (sent.append(text) or "plain answer"), prompts=["Return JSON"])
    assert output == ["plain answer"] and len(sent) == 1


def test_invalid_output_reference_is_rejected_before_any_request():
    with pytest.raises(InputError):
        MinimalChainable.run({}, None, llm_callable=lambda *_: pytest.fail("A forward reference dispatched"), prompts=["First", "Use {{output[0]}}"])


def test_framework_inserts_inputs_once_and_quotes_literal_examples():
    sent = []
    responses = iter(["literal {{output[-1]}}", "done"])
    def answer(_, prompt):
        sent.append(prompt)
        return next(responses), {}
    MinimalChainable.run({"topic": "literal {{output[-1]}}"}, None, llm_callable=answer,
                         prompts=["Read {{topic}}; literal example {{{{output[-1]}}}}", "Use {{output[-1]}}"])
    assert sent == ["Read literal {{output[-1]}}; literal example {{output[-1]}}", "Use literal {{output[-1]}}"]


@pytest.mark.parametrize("registry,name", [(natural_reasoning.REASONING_PATTERNS, name) for name in natural_reasoning.REASONING_PATTERNS] +
                         [(adversarial_chains.ADVERSARIAL_PATTERNS, name) for name in adversarial_chains.ADVERSARIAL_PATTERNS])
def test_displayed_request_plan_matches_generated_pattern_steps(monkeypatch, registry, name):
    captured = []
    def execute(_, prompts, **kwargs):
        captured.extend(prompts)
        return [{} for _ in prompts], []
    monkeypatch.setattr(natural_reasoning, "execute_pattern", execute)
    monkeypatch.setattr(adversarial_chains, "execute_pattern", execute)
    schema = registry[name]["input_schema"]
    payload = {key: "A question" for key, value in schema.items() if value.get("required")}
    kwargs = advanced.normalize_payload(registry, name, payload)
    registry[name]["function"](**kwargs)
    assert advanced.planned_requests(name, kwargs) == len(captured)


def test_reasoning_handoffs_use_actual_earlier_answers(monkeypatch):
    monkeypatch.setattr(MinimalChainable, "log_to_markdown", lambda *_: "")
    sent = []
    def answer(_, prompt):
        sent.append(prompt)
        return '{"cause":"actual previous cause","root_cause":"unestablished","winner":"Neither"}', {}
    natural_reasoning.five_whys("test", depth=2, model_info=(None, "offline"), llm_callable=answer)
    assert "Previous cause: actual previous cause" in sent[2]
    assert '"is_root_cause": false' in sent[2]
    sent.clear()
    adversarial_chains.red_vs_blue("test", "test", rounds=1, model_info=(None, "offline"), llm_callable=answer)
    assert "actual previous cause" in sent[-1]
    assert "{{output[0]}}" not in sent[-1]


def test_meta_fallback_includes_the_actual_analysis(tmp_path, monkeypatch):
    generator = MetaChainGenerator(artifact_store=ArtifactStore(str(tmp_path / "artifacts")), model_info=(None, "offline"))
    with monkeypatch.context() as patch:
        patch.setattr(MinimalChainable, "run", lambda **_: (["bad analysis", "bad design"], [], []))
        design = generator.design_chain("A goal")
    sent = []
    MinimalChainable.run({}, None, llm_callable=lambda _, text: (sent.append(text) or "actual first answer"), prompts=design.prompts)
    assert "actual first answer" in sent[1]


def test_large_workspace_backup_round_trips_and_rejects_oversized_json(tmp_path):
    source = Store(tmp_path / "source")
    recipe = Recipe(title="Bounded", steps=[Step(name=str(i), prompt="{{topic}}") for i in range(8)])
    for _ in range(8):
        source.create_run(Run(recipe=recipe, topic="Large", state="completed", results=[Result(prompt="p" * 120000, output="a" * 60000) for _ in range(8)]))
    with pytest.raises(ValueError, match="restore limit"):
        source.backup()
    archive = source.archive()
    destination = Store(tmp_path / "destination")
    assert destination.restore(archive) == (0, 8)
    assert destination.restore(archive) == (0, 0)
    assert destination.get_run(source.runs()[0].id).model_dump() == source.runs()[0].model_dump()


def test_archive_supports_more_than_2000_records(tmp_path):
    store = Store(tmp_path / "source")
    recipe = Recipe(title="Reusable", steps=[Step(name="Start", prompt="{{topic}}")])
    records = [SavedRecipe(recipe=recipe) for _ in range(2001)]
    with store.connection() as db:
        db.executemany("INSERT INTO recipes VALUES (?, ?)", [(r.id, r.model_dump_json()) for r in records])
    raw = store.archive()
    destination = Store(tmp_path / "destination")
    assert destination.restore(raw) == (2001, 0)


def test_archive_validates_all_parts_before_importing(tmp_path):
    store = Store(tmp_path / "source")
    store.save_recipe(Recipe(title="Recipe", steps=[Step(name="Start", prompt="{{topic}}")]))
    raw = store.archive()
    target = BytesIO()
    with zipfile.ZipFile(BytesIO(raw)) as source, zipfile.ZipFile(target, "w") as corrupt:
        for name in source.namelist():
            corrupt.writestr(name, b"corrupt" if name.endswith("0001.json") else source.read(name))
    destination = Store(tmp_path / "destination")
    with pytest.raises(ValueError, match="No records"):
        destination.restore(target.getvalue())
    assert destination.recipes() == []


def test_export_refuses_a_recipe_its_importer_cannot_accept(tmp_path):
    store = Store(tmp_path / "workspace")
    store.save_recipe(Recipe(title="Invalid handoff", steps=[Step(name="Start", prompt="{{output[-1]}}")]))
    with pytest.raises(ValueError, match="invalid recipe reference"):
        store.archive()


def test_tool_prefers_saved_json_and_omits_private_process_diagnostics(tmp_path, monkeypatch):
    output = tmp_path / "output/result.json"
    output.parent.mkdir()
    output.write_text('{"answer":"kept"}')
    log = tmp_path / "logs/result.md"
    log.parent.mkdir()
    log.write_text("PRIVATE_PROCESS_TEXT")
    monkeypatch.setattr(advanced.subprocess, "run", lambda *_, **__: SimpleNamespace(returncode=0, stdout=f"✅ Saved JSON to: {output}\n✅ Log saved to: {log}\nPRIVATE_PROCESS_TEXT", stderr="PRIVATE_PROCESS_TEXT"))
    result = advanced.execute_tool("installed.py", str(tmp_path), "learning", "concept_simplifier", "A topic")
    assert result["type"] == "json" and result["output"] == {"answer": "kept"}
    assert "PRIVATE_PROCESS_TEXT" not in json.dumps(result)


def test_tool_failure_keeps_subprocess_payload_private(tmp_path, monkeypatch):
    monkeypatch.setattr(advanced.subprocess, "run", lambda *_, **__: SimpleNamespace(returncode=1, stdout="PRIVATE_PROCESS_TEXT", stderr="PRIVATE_PROCESS_TEXT"))
    with pytest.raises(InputError) as error:
        advanced.execute_tool("installed.py", str(tmp_path), "learning", "concept_simplifier", "A topic")
    assert "PRIVATE_PROCESS_TEXT" not in str(error.value)


def test_cli_zip_backup_round_trip_does_not_call_provider(tmp_path, monkeypatch):
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "source"))
    monkeypatch.setattr(llm_client, "build_models", lambda: pytest.fail("Backup called a provider"))
    path = tmp_path / "copy.zip"
    assert studio.main(["backup", str(path)]) == 0
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "destination"))
    assert studio.main(["restore", str(path)]) == 0
    assert studio.main(["backup", str(path)]) == 1


def test_composer_accounting_and_trace_are_independent_per_call(tmp_path):
    composer = ChainComposer(artifact_store=ArtifactStore(str(tmp_path / "artifacts")), model_info=(None, "offline"), llm_callable=lambda *_: ("answer", {"prompt_tokens": 2, "completion_tokens": 3}))
    first = composer.compose([ChainStep("First", "chain", prompts=["First prompt"])])
    second = composer.compose([ChainStep("Second", "chain", prompts=["Second prompt"])])
    assert first.total_tokens == second.total_tokens == 5
    assert first.execution_trace[0]["trace"]["steps"][0]["prompt"] == "First prompt"
    assert second.execution_trace[0]["trace"]["steps"][0]["prompt"] == "Second prompt"
    assert first.total_cost is None


def test_failed_chain_is_not_judged_and_batch_excludes_failures():
    def fail(*_, **__):
        raise RuntimeError("PRIVATE_FAILURE")
    result, metadata = comparisons.measure_emergence("topic", fail, model_info=(None, "offline"), llm_callable=lambda *_: pytest.fail("A failed chain triggered baseline or judge"))
    assert result["status"] == "failed" and result["winner"] == "Inconclusive"
    assert "PRIVATE_FAILURE" not in json.dumps((result, metadata))
    aggregate, _ = comparisons.batch_measure(["one", "two"], fail, model_info=(None, "offline"), llm_callable=lambda *_: pytest.fail("A failed chain dispatched"))
    assert aggregate["comparisons_scored"] == 0
    assert aggregate["failed_comparisons"] == 2
    assert aggregate["results"]["ties"] == 0
    assert "no statistical significance test" in aggregate["statistical_significance"]


@pytest.mark.parametrize("value", [True, "10", float("nan"), -1, 11])
def test_bad_judge_scores_never_produce_a_winner(value):
    scores = {side: {key: 5 for key in ("novelty", "depth", "coherence", "pedagogical", "actionability")} for side in ("approach_a", "approach_b")}
    scores["approach_a"]["novelty"] = value
    assert comparisons._determine_winner({"scores": scores}) == "Inconclusive"


def test_energy_setting_changes_actual_generation_constraints(monkeypatch):
    sent = []
    def run(**kwargs):
        sent.append(kwargs["prompts"])
        return ["---\n## Problem\n## Prompt\n## Examples\n" + "Draft " * 100], [], [], {}
    monkeypatch.setattr(ms_content_tools, "get_model", lambda: (None, "offline"))
    monkeypatch.setattr(MinimalChainable, "run", run)
    monkeypatch.setattr(MinimalChainable, "log_to_markdown", lambda *_: "")
    ms_content_tools.generate_prompt_card("A job", energy_level="low")
    ms_content_tools.generate_prompt_card("A job", energy_level="high")
    assert "under 600 words" in sent[0][-1]
    assert "under 1200 words" in sent[1][-1]
    assert "illustrative" in sent[0][-1]


@pytest.mark.parametrize("function,kwargs", [(ms_content_tools.generate_shortcut_spotlight, {"tool": "A tool", "ms_benefit": "A supplied constraint"}),
                                            (ms_content_tools.generate_guide, {"system": "A system"})])
def test_content_generators_keep_draft_contract_and_no_invented_measurements(monkeypatch, function, kwargs):
    prompts = []
    def run(**fields):
        prompts.extend(fields["prompts"])
        return ["---\n## Quick Path\n## Phase\n## Troubleshooting\n" + "Draft " * 100], [], [], {}
    monkeypatch.setattr(ms_content_tools, "get_model", lambda: (None, "offline"))
    monkeypatch.setattr(MinimalChainable, "run", run)
    monkeypatch.setattr(MinimalChainable, "log_to_markdown", lambda *_: "")
    content, metadata = function(**kwargs)
    assert isinstance(content, str) and isinstance(metadata, dict)
    assert any("invent" in prompt.lower() and ("measured" in prompt.lower() or "measurement" in prompt.lower()) for prompt in prompts)


def test_logs_and_cost_report_distinguish_unknown_from_estimate(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(chain, "__file__", str(tmp_path / "lib/core/chain.py"))
    monkeypatch.delenv("LOG_INPUT_TOKEN_PRICE_PER_MILLION", raising=False)
    monkeypatch.delenv("LOG_OUTPUT_TOKEN_PRICE_PER_MILLION", raising=False)
    path = MinimalChainable.log_to_markdown("test", ["prompt"], ["answer"], [{"prompt_tokens": 2, "completion_tokens": 3}])
    assert "Unknown" in Path(path).read_text()
    assert cost_report.parse_cost_from_log(path) is None
    monkeypatch.setenv("LOG_INPUT_TOKEN_PRICE_PER_MILLION", "1")
    monkeypatch.setenv("LOG_OUTPUT_TOKEN_PRICE_PER_MILLION", "2")
    priced = MinimalChainable.log_to_markdown("priced", ["prompt"], ["answer"], [{"prompt_tokens": 2, "completion_tokens": 3}])
    assert cost_report.parse_cost_from_log(priced) == pytest.approx(.000008)
    monkeypatch.setattr(cost_report, "project_root", str(tmp_path))
    cost_report.generate_cost_report()
    output = capsys.readouterr().out
    assert "TOTAL ESTIMATED COST" in output and "unknown or unreadable: 1" in output
    assert "TOTAL SPEND" not in output
