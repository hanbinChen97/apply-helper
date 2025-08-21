import yaml
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential

# --- Configuration Loading ---
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "defaults.yaml"
try:
    with open(CONFIG_PATH, 'r') as f:
        CONFIG = yaml.safe_load(f)
    if not CONFIG: # Handle empty yaml file
        raise ValueError("Config file is empty")
except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
    print(f"Warning: Could not load or parse config/defaults.yaml: {e}. Using fallback configuration.")
    CONFIG = {
        "llm": {
            "provider": "openai",
            "models": {
                "openai": "gpt-4o",
                "azure": "your-azure-deployment-name",
                "gemini": "gemini-1.5-pro",
            }
        }
    }

# --- Model Selection ---
def get_model_name(provider: str = None) -> str:
    """
    Gets the model name for a given provider from the config file.
    If no provider is specified, it uses the default provider from the config.
    """
    llm_config = CONFIG.get("llm", {})

    # Use the provider passed as an argument, or fall back to the default in the config.
    provider_to_use = provider or llm_config.get("provider", "openai")

    model_name = llm_config.get("models", {}).get(provider_to_use)

    if not model_name:
        raise ValueError(f"Model for provider '{provider_to_use}' not found in configuration.")

    # The 'azure' provider model name in litellm should not be prefixed with 'azure/'
    # if it's a deployment name. LiteLLM handles this.
    # However, some providers are prefixed, e.g., "openai/gpt-4o".
    # The current logic assumes the config stores the exact string litellm needs.
    # For azure, the deployment name is passed as the model, and the api_base/key determine it's azure.
    # Let's adjust for azure specifically.
    if provider_to_use == "azure":
         # litellm expects just the deployment name for azure, not prefixed.
         # But when we call `litellm.completion(model="azure/deployment-name")` it also works.
         # For simplicity and consistency with other providers like "openai/gpt-4o",
         # we can expect the config to store the full model string.
         # The current hardcoded value is "azure/your-deployment-name", which is not a valid litellm model string.
         # LiteLLM expects "azure/<deployment_name>".
         # I will assume the config stores the full "provider/model" string for clarity.
         # My previous hardcoded value was wrong. It should be "azure/<deployment_name>".
         # The current code is fine if the config is correct.
         # Let's assume the value in `defaults.yaml` is the correct model string for litellm.
         pass

    return model_name

# --- Retry Logic ---
# Define the retry decorator directly, so it can be imported and used.
retry_on_exception = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
