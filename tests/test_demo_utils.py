import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.utils import demo_utils
from lib.utils.demo_examples import (
    get_adversarial_demo_examples,
    get_meta_demo_examples,
    get_reasoning_demo_examples,
    get_tool_demo_examples,
)

class TestDemoUtils(unittest.TestCase):
    
    def test_setup_demo_env_adds_path(self):
        # Use a real list for sys.path to verify modification
        real_sys_path = []
        with patch('sys.path', real_sys_path):
            demo_utils.setup_demo_env()

        expected_root = str(Path(demo_utils.__file__).resolve().parents[2])
        self.assertIn(expected_root, real_sys_path)

    @patch('os.path.exists')
    @patch('lib.utils.demo_utils.load_dotenv')
    @patch('os.getenv')
    def test_setup_demo_env_loads_dotenv(self, mock_getenv, mock_load_dotenv, mock_exists):
        # Setup
        mock_exists.return_value = True
        mock_getenv.return_value = "fake_key" # Simulate API key existing
        
        # Run
        result = demo_utils.setup_demo_env()
        
        # Verify
        mock_load_dotenv.assert_called()
        self.assertTrue(result)

    @patch('os.getenv')
    def test_setup_demo_env_missing_api_key(self, mock_getenv):
        # Setup
        mock_getenv.return_value = None # Simulate missing key
        
        # Run
        # We expect it to print error messages, but we won't capture stdout here for simplicity
        result = demo_utils.setup_demo_env()
        
        # Verify
        self.assertFalse(result)

    def test_tool_demo_examples_fall_back_to_available_tool(self):
        examples = get_tool_demo_examples(["learning:concept_simplifier"])

        self.assertEqual(len(examples), 5)
        self.assertTrue(
            all(example["fields"]["tool_key"] == "learning:concept_simplifier" for example in examples)
        )

    def test_reasoning_demo_examples_cover_all_patterns(self):
        pattern_names = {example["fields"]["pattern_name"] for example in get_reasoning_demo_examples()}

        self.assertEqual(len(pattern_names), 5)
        self.assertIn("scientific_method", pattern_names)
        self.assertIn("five_whys", pattern_names)

    def test_adversarial_and_meta_demo_examples_have_five_entries(self):
        self.assertEqual(len(get_adversarial_demo_examples()), 5)
        self.assertEqual(len(get_meta_demo_examples()), 5)

if __name__ == '__main__':
    unittest.main()
