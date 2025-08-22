import litellm
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key for OpenAI
litellm.api_key = os.getenv("OPENAI_API_KEY")

def call_llm(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Calls the LLM API using LiteLLM.

    Args:
        prompt: The prompt to send to the LLM.
        model: The model to use for the completion.

    Returns:
        The content of the LLM's response message.

    Raises:
        Exception: If the LiteLLM API call fails.
    """
    try:
        messages = [{"role": "user", "content": prompt}]
        response = litellm.completion(model=model, messages=messages)
        content = response["choices"][0]["message"]["content"]
        if not content:
            raise ValueError("Received an empty response from the LLM.")
        return content
    except Exception as e:
        # In a real application, you'd have more robust logging and error handling.
        print(f"An error occurred while calling the LLM: {e}")
        raise
