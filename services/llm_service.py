import json
from typing import Tuple, Dict, Any

from llm.litellm_client import call_llm
from llm.prompt_templates import get_template

def _parse_json_response(response: str) -> Dict[str, Any]:
    """
    Parses a JSON string from the LLM response.
    """
    try:
        # The LLM might return a string enclosed in ```json ... ```, so we find the JSON block.
        json_block = response[response.find('{'):response.rfind('}')+1]
        return json.loads(json_block)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Failed to parse JSON response: {e}\nResponse was: {response}")
        raise ValueError("LLM response was not in the expected JSON format.")


def analyse_llm(jd: str, user_info: str) -> Dict[str, Any]:
    """
    Calls the LLM to analyse the JD and user info.
    """
    prompt = get_template("analyse").format(jd=jd, user=user_info)
    response_text = call_llm(prompt)
    return _parse_json_response(response_text)


def refine_llm(summary: Dict[str, Any], feedback: str) -> Dict[str, Any]:
    """
    Calls the LLM to refine an existing analysis based on user feedback.
    """
    summary_str = json.dumps(summary, indent=2)
    prompt = get_template("refine").format(summary=summary_str, feedback=feedback)
    response_text = call_llm(prompt)
    return _parse_json_response(response_text)


def generate_resume_llm(summary: Dict[str, Any], user_info: str) -> str:
    """
    Calls the LLM to generate a resume.
    """
    summary_str = json.dumps(summary, indent=2)
    prompt = get_template("generate_resume").format(summary=summary_str, user=user_info)
    return call_llm(prompt)


def generate_cover_letter_llm(summary: Dict[str, Any], user_info: str) -> str:
    """
    Calls the LLM to generate a cover letter.
    """
    summary_str = json.dumps(summary, indent=2)
    prompt = get_template("generate_cover_letter").format(summary=summary_str, user=user_info)
    return call_llm(prompt)
