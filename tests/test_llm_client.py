import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm.client import chat_complete
from src.core.errors import InvalidJSONResponseError, LLMError

@patch('src.llm.client.litellm.completion')
def test_chat_complete_text_success(mock_completion):
    """Tests a successful text completion."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "This is a test response."
    mock_completion.return_value = mock_response

    response = chat_complete(messages=[{"role": "user", "content": "test"}])

    assert response == "This is a test response."
    mock_completion.assert_called_once()

@patch('src.llm.client.litellm.completion')
def test_chat_complete_json_success(mock_completion):
    """Tests a successful JSON completion."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"key": "value"}'
    mock_completion.return_value = mock_response

    response = chat_complete(messages=[{"role": "user", "content": "test"}], response_format="json")

    assert response == {"key": "value"}
    assert mock_completion.call_count == 1

@patch('src.llm.client.litellm.completion')
def test_chat_complete_invalid_json_raises_error(mock_completion):
    """Tests that invalid JSON raises the correct error."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = 'this is not json'
    mock_completion.return_value = mock_response

    with pytest.raises(InvalidJSONResponseError):
        chat_complete(messages=[{"role": "user", "content": "test"}], response_format="json")

    assert mock_completion.call_count > 1

@patch('src.llm.client.litellm.completion')
def test_chat_complete_llm_failure_raises_error(mock_completion):
    """Tests that a failure in the underlying litellm call raises LLMError."""
    mock_completion.side_effect = Exception("Something went wrong with the API")

    with pytest.raises(LLMError):
        chat_complete(messages=[{"role": "user", "content": "test"}])

    assert mock_completion.call_count > 1
