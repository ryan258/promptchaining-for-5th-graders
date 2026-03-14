import json
from pathlib import Path

from fastapi.testclient import TestClient

import server.main as server_main
from lib.enhancements.adversarial_chains import ADVERSARIAL_PATTERNS
from lib.enhancements.natural_reasoning import REASONING_PATTERNS


client = TestClient(server_main.app)


def test_ui_index_renders():
    response = client.get("/")

    assert response.status_code == 200
    assert "Prompt Chaining Studio" in response.text
    assert "/studio/reasoning" in response.text


def test_studio_pages_render():
    pages = [
        ("/studio/tools", "Run a Tool"),
        ("/studio/reasoning", "Reasoning Patterns"),
        ("/studio/adversarial", "Adversarial Patterns"),
        ("/studio/meta", "Meta-Chain Designer"),
        ("/studio/artifacts", "Artifacts Library"),
    ]

    for path, marker in pages:
        response = client.get(path)

        assert response.status_code == 200
        assert marker in response.text


def test_tools_endpoint_hides_internal_path():
    response = client.get("/tools")

    assert response.status_code == 200
    tools = response.json()
    assert tools
    assert "path" not in tools[0]


def test_scan_tools_is_cached(monkeypatch):
    tool_paths = [
        str(Path(server_main.TOOLS_DIR) / "learning" / "concept_simplifier.py"),
        str(Path(server_main.TOOLS_DIR) / "learning" / "subject_connector.py"),
    ]
    calls = {"count": 0}

    def fake_glob(_pattern):
        calls["count"] += 1
        return tool_paths

    server_main._scan_tools.cache_clear()
    monkeypatch.setattr(server_main.glob, "glob", fake_glob)

    client.get("/tools")
    client.get("/tools")

    assert calls["count"] == 1


def test_artifacts_endpoint_filters_internal_files(tmp_path, monkeypatch):
    artifacts_dir = tmp_path / "artifacts"
    topic_dir = artifacts_dir / "science"
    topic_dir.mkdir(parents=True)
    (topic_dir / "summary.json").write_text('{"ok": true}', encoding="utf-8")
    (topic_dir / "summary.meta.json").write_text('{"internal": true}', encoding="utf-8")
    chroma_dir = artifacts_dir / "_chroma"
    chroma_dir.mkdir()
    (chroma_dir / "index.bin").write_text("internal", encoding="utf-8")

    monkeypatch.setattr(server_main, "ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setattr(server_main, "ARTIFACTS_ROOT", artifacts_dir.resolve())

    response = client.get("/artifacts")

    assert response.status_code == 200
    payload = response.json()
    assert payload == [
        {
            "topic": "science",
            "filename": "summary.json",
            "size": len('{"ok": true}'),
            "modified": payload[0]["modified"],
        }
    ]


def test_artifact_endpoint_rejects_internal_topic(tmp_path, monkeypatch):
    artifacts_dir = tmp_path / "artifacts"
    monkeypatch.setattr(server_main, "ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setattr(server_main, "ARTIFACTS_ROOT", artifacts_dir.resolve())

    response = client.get("/artifacts/_chroma/index.bin")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid artifact path"


def test_pattern_route_returns_400_for_bad_depth():
    response = client.post("/patterns/five_whys", json={"topic": "Missed homework", "depth": "oops"})

    assert response.status_code == 400
    assert "Invalid value for depth" in response.json()["detail"]


def test_pattern_payload_coerces_string_to_string_list():
    normalized = server_main._normalize_registry_payload(
        REASONING_PATTERNS,
        "scientific_method",
        {"topic": "Gravity", "evidence_sources": "textbook"},
    )

    assert normalized["hypothesis"] == "Gravity"
    assert normalized["evidence_sources"] == ["textbook"]


def test_adversarial_payload_coerces_false_string_to_bool():
    normalized = server_main._normalize_registry_payload(
        ADVERSARIAL_PATTERNS,
        "adversarial_socratic",
        {"topic": "Claim", "aggressive": "false"},
    )

    assert normalized["claim"] == "Claim"
    assert normalized["aggressive"] is False


def test_emergence_route_passes_explicit_chain_name(monkeypatch):
    captured = {}

    def fake_measure_emergence(**kwargs):
        captured.update(kwargs)
        return {"winner": "Chain"}, {"chain_function": kwargs["chain_name"]}

    monkeypatch.setattr(server_main, "measure_emergence", fake_measure_emergence)

    response = client.post(
        "/emergence/compare",
        json={"topic": "Neural Networks", "chain_name": "scientific_method"},
    )

    assert response.status_code == 200
    assert captured["chain_name"] == "scientific_method"
    assert captured["hypothesis"] == "Neural Networks"


def test_ui_meta_execute_surfaces_http_exception_detail():
    response = client.post("/ui/meta-execute", data={"design_json": json.dumps({"goal": "Test"})})

    assert response.status_code == 200
    assert "Design must include prompts to execute" in response.text


def test_ui_run_pattern_accepts_plain_text_fields(monkeypatch):
    captured = {}

    def fake_execute_pattern(pattern_name, payload):
        captured["pattern_name"] = pattern_name
        captured["payload"] = payload
        return {
            "pattern": pattern_name,
            "result": {"summary": "ok"},
            "metadata": {},
        }

    monkeypatch.setattr(server_main, "_execute_pattern", fake_execute_pattern)

    response = client.post(
        "/ui/run-pattern",
        data={
            "pattern_name": "scientific_method",
            "hypothesis": "Plants grow better with more sunlight",
            "evidence_sources": "Science textbook\nClassroom experiment",
        },
    )

    assert response.status_code == 200
    assert captured["pattern_name"] == "scientific_method"
    assert captured["payload"]["hypothesis"] == "Plants grow better with more sunlight"
    assert captured["payload"]["evidence_sources"] == [
        "Science textbook",
        "Classroom experiment",
    ]


def test_ui_meta_design_accepts_plain_text_context(monkeypatch):
    captured = {}

    class FakeDesign:
        def to_dict(self):
            return {
                "goal": "Teach fractions",
                "reasoning": "Use concrete analogies first.",
                "cognitive_moves": ["Break concept down"],
                "prompts": ["Explain fractions with baseball examples."],
                "context": captured["context"],
                "metadata": {},
            }

    class FakeGenerator:
        def design_chain(self, goal, context, constraints):
            captured["goal"] = goal
            captured["context"] = context
            captured["constraints"] = constraints
            return FakeDesign()

    monkeypatch.setattr(server_main, "MetaChainGenerator", FakeGenerator)

    response = client.post(
        "/ui/meta-design",
        data={
            "goal": "Teach fractions",
            "context_text": "audience: 5th graders\nUse sports examples",
            "constraints": "Keep it visual\nUse familiar language",
        },
    )

    assert response.status_code == 200
    assert captured["goal"] == "Teach fractions"
    assert captured["context"] == {
        "audience": "5th graders",
        "notes": "Use sports examples",
    }
    assert captured["constraints"] == ["Keep it visual", "Use familiar language"]
    assert "Execute This Chain" in response.text
