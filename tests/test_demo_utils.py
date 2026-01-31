import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.utils import demo_utils

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

if __name__ == '__main__':
    unittest.main()
