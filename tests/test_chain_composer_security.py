from pathlib import Path

from lib.core.artifact_store import ArtifactStore
from lib.core.chain_composer import ChainComposer, ChainStep


def test_find_tool_path_rejects_path_traversal():
    composer = ChainComposer(model_info=("mock-client", "mock-model"), llm_callable=lambda *_: ("{}", {}))

    assert composer._find_tool_path("../../server/main") is None


def test_tool_step_uses_function_signature(monkeypatch, tmp_path):
    tool_path = tmp_path / "temp_tool.py"
    tool_path.write_text(
        "\n".join(
            [
                '"""Temp tool for tests."""',
                "def temp_tool(topic, note='', artifact_store=None):",
                "    artifact_store.save(topic, 'note', {'note': note})",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "lib.core.chain_composer._discover_tool_registry",
        lambda: {"temp_tool": str(tool_path)},
    )

    store = ArtifactStore(base_dir=str(tmp_path / "artifacts"))
    composer = ChainComposer(
        artifact_store=store,
        model_info=("mock-client", "mock-model"),
        llm_callable=lambda *_: ("{}", {}),
    )

    result = composer.compose(
        [
            ChainStep(
                name="Temp tool",
                step_type="tool",
                tool_name="temp_tool",
                tool_args={"topic": "science", "note": "hello", "ignored": "value"},
            )
        ]
    )

    assert result.steps_executed[0]["tool_name"] == "temp_tool"
    assert store.get("science", "note") == {"note": "hello"}
