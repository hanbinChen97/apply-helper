import json
import litellm
from typing import List, Dict, Optional, Union

from src.core.errors import InvalidJSONResponseError, LLMError
from src.core.logger import get_logger
from src.llm.router import get_model_name, retry_on_exception

logger = get_logger(__name__)

@retry_on_exception
def chat_complete(
    messages: List[Dict[str, str]],
    response_format: str = "text",
    system_prompt: Optional[str] = None,
    provider: str = "openai",
) -> Union[Dict, str]:
    """
    Generates a chat completion using the specified provider.
    This function is decorated with a retry mechanism.
    """
    model = get_model_name(provider)

    all_messages = messages
    if system_prompt:
        all_messages = [{"role": "system", "content": system_prompt}] + messages

    try:
        logger.info(f"Calling LLM {model} with {len(all_messages)} messages.")

        litellm_params = {
            "model": model,
            "messages": all_messages,
        }

        if response_format == "json":
            litellm_params["response_format"] = {"type": "json_object"}

        response = litellm.completion(**litellm_params)

        content = response.choices[0].message.content

        if content is None:
            raise LLMError("LLM response content is empty.")

        if response_format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM response as JSON. Response: {content}")
                raise InvalidJSONResponseError(response_text=content)
        else:
            return content

    except Exception as e:
        if isinstance(e, (InvalidJSONResponseError, LLMError)):
            raise

        logger.error(f"An unexpected error occurred during LLM call: {e}", exc_info=True)
        raise LLMError("LLM call failed after retries.") from e
