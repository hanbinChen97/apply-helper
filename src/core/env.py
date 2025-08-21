import os
from dotenv import load_dotenv

def load_environment():
    """Loads environment variables from a .env file."""
    load_dotenv()

# Call it on import to make sure variables are loaded when the module is imported
load_environment()

def get_env_variable(variable_name: str, default: str = "") -> str:
    """Gets an environment variable, with a fallback to a default value."""
    return os.getenv(variable_name, default)
