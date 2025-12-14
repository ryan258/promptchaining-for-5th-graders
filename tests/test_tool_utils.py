
import os
import json
import shutil
import pytest
from unittest.mock import MagicMock, patch
from tools.tool_utils import save_chain_output

@pytest.fixture
def mock_chainable():
    with patch('src.core.chain.MinimalChainable') as mock:
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
