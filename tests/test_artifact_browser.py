import json

from lib.utils import artifact_browser


class FakeStore:
    def list_topics(self):
        return ["science"]

    def list_steps_for_topic(self, topic):
        return ["summary"] if topic == "science" else []

    def get(self, topic, step):
        return {"topic": topic, "step": step}

    def get_metadata(self, _topic, _step):
        return {"created_at": "2026-03-14T12:00:00", "artifacts_used": ["science:summary"]}

    def visualize(self):
        return "science"


def test_show_topic_artifacts_prints_content(capsys):
    artifact_browser.show_topic_artifacts(FakeStore(), "science")

    output = capsys.readouterr().out
    assert "SCIENCE" in output
    assert '"topic": "science"' in output


def test_export_topic_writes_json_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(artifact_browser, "ArtifactStore", FakeStore)

    artifact_browser.export_topic("science")

    export_path = tmp_path / "science_export.json"
    assert export_path.exists()
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["topic"] == "science"
    assert payload["artifacts"]["summary"]["data"]["topic"] == "science"
