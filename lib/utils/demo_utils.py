import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def setup_demo_env():
    """
    Sets up the environment for running a demo.
    - Adds project root to sys.path
    - Loads .env file
    - Checks for API key
    """
    # Add project root to sys.path (lib/utils -> lib -> repo root)
    project_root = Path(__file__).resolve().parents[2]
    
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    
    # Load .env
    dotenv_path = os.path.join(project_root_str, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found in .env file.")
        print("Please copy .env.example to .env and add your API key.")
        return False
        
    return True
