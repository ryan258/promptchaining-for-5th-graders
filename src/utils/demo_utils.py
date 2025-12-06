import os
import sys
from dotenv import load_dotenv

def setup_demo_env():
    """
    Sets up the environment for running a demo.
    - Adds project root to sys.path
    - Loads .env file
    - Checks for API key
    """
    # Add project root to sys.path
    # We assume this file is in the project root or we can find it relative to the demo
    # But since this utils file is in the project root, we can just use its location
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Load .env
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found in .env file.")
        print("Please copy .env.example to .env and add your API key.")
        return False
        
    return True
