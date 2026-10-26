import json

import pytest

from lib.core.llm_client import build_models, get_prompt_settings


@pytest.fixture(autouse=True)
def clear_llm_client_caches():
    build_models.cache_clear()
    get_prompt_settings.cache_clear()
    yield
    build_models.cache_clear()
    get_prompt_settings.cache_clear()


@pytest.fixture
def mock_model_info():
    return ("mock-client", "mock-model")


@pytest.fixture
def mock_usage():
    return {"prompt_tokens": 11, "completion_tokens": 7}


@pytest.fixture
def sequence_llm(mock_usage):
    def factory(responses):
        queue = list(responses)

        def _call(_model, _prompt):
            if not queue:
                raise AssertionError("No more mocked LLM responses available")

            response = queue.pop(0)
            if not isinstance(response, str):
                response = json.dumps(response)
            return response, mock_usage

        return _call

    return factory


@pytest.fixture(autouse=True)
def isolate_default_artifacts(tmp_path, monkeypatch):
    """Library examples in tests must never write into Ryan's artifact library."""
    from lib.core.artifact_store import ArtifactStore
    original = ArtifactStore.__init__

    def initialize(self, base_dir="artifacts"):
        if str(base_dir) == "artifacts":
            base_dir = tmp_path / "artifacts"
        original(self, base_dir=base_dir)

    monkeypatch.setattr(ArtifactStore, "__init__", initialize)
