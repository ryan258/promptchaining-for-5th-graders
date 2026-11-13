
import os
import json
import shutil
import pytest
from unittest.mock import MagicMock, patch
from tools.cost_report import parse_cost_from_log
from tools.tool_utils import learning_profile_fields, save_chain_output

@pytest.fixture
def mock_chainable():
    with patch('lib.core.chain.MinimalChainable') as mock:
        mock.log_to_markdown.return_value = "mock_log.md"
        yield mock

def test_save_chain_output_structure(tmp_path, mock_chainable):
    """Verify that save_chain_output creates the expected file structure."""
    
    # Setup inputs
    project_root = str(tmp_path)
    output_dir = os.path.join(project_root, "output", "test_tool")
    tool_name = "test_tool"
    topic = "Testing Magic"
    execution_trace = {"steps": [], "result": "Success"}
    result = "Success"
    context_filled_prompts = ["Prompt 1"]
    usage_stats = {"total_tokens": 100}
    
    # Execute
    json_path, log_path = save_chain_output(
        project_root, 
        output_dir, 
        tool_name, 
        topic, 
        execution_trace, 
        result, 
        context_filled_prompts, 
        usage_stats
    )
    
    # Verify outputs
    assert json_path is not None
    assert log_path == "mock_log.md"
    assert os.path.exists(output_dir)
    
    # Check JSON content
    files = os.listdir(output_dir)
    json_files = [f for f in files if f.endswith('.json')]
    assert len(json_files) == 1
    
    with open(os.path.join(output_dir, json_files[0]), 'r') as f:
        data = json.load(f)
        assert data == execution_trace

def test_save_chain_output_sanitization(tmp_path, mock_chainable):
    """Verify filename sanitization."""
    project_root = str(tmp_path)
    output_dir = os.path.join(project_root, "output")
    topic = "Crazy / Topic : With * Symbols?"
    
    save_chain_output(
        project_root, 
        output_dir, 
        "tool", 
        topic, 
        {}, 
        "", 
        [], 
        {}
    )
    
    generated_file = [f for f in os.listdir(output_dir) if f.endswith('.json')][0]
    assert "/" not in generated_file
    assert ":" not in generated_file
    assert "?" not in generated_file
    # Check that it replaced chars with _ (or removed them depending on impl)
    assert "Crazy___Topic___With___Symbols_" in generated_file or "Crazy" in generated_file


def test_cost_report_ignores_prices_in_prompt_or_answer(tmp_path):
    log = tmp_path / "result.md"
    log.write_text("# Chain log\n**Estimated Cost**: Unknown\n\n## AI responses\n**Estimated Cost**: $99.00\n")
    assert parse_cost_from_log(log) is None


def test_learning_profile_uses_only_its_declared_fields(tmp_path):
    profile = tmp_path / "context" / "user_profile.json"
    profile.parent.mkdir()
    profile.write_text('{"writing_style":{"tone":" Precise "},"learning_profile":{"audience": []},"private":"other"}')
    assert learning_profile_fields(tmp_path) == {"tone": "Precise", "audience": "Curious adult"}
    assert learning_profile_fields(tmp_path, connector=True) == {"tone": "Precise"}
    profile.write_text("{broken")
    assert learning_profile_fields(tmp_path, connector=True) == {"tone": "Clear and practical"}
