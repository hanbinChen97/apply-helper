from pathlib import Path
from typing import Tuple

from src.core.schemas import JobDescription, UserInfo, AnalyseSummary

PROMPTS_DIR = Path(__file__).parent.parent.parent / "config" / "prompts"

def _read_prompt_template(filename: str) -> str:
    """Reads a prompt template from the config/prompts directory."""
    filepath = PROMPTS_DIR / filename
    try:
        return filepath.read_text()
    except FileNotFoundError:
        # In a real app, you might want to log this error more formally.
        print(f"Error: Prompt template '{filename}' not found at {filepath}")
        return f"Error: Prompt template '{filename}' not found."


def compose_analyse_prompt(jd: JobDescription, user: UserInfo) -> Tuple[str, str]:
    """Composes the prompt for the analysis step."""
    system_prompt = _read_prompt_template("analyse_system.md")
    user_template = _read_prompt_template("analyse_user.md")

    # Assuming the user_template has placeholders for job_description and user_info
    user_prompt = user_template.format(
        job_description=jd.raw_text,
        user_info=user.resume_text
    )
    return system_prompt, user_prompt

def compose_refine_prompt(summary: AnalyseSummary, feedback: str) -> str:
    """Composes the prompt for the refinement step."""
    refine_template = _read_prompt_template("refine_user.md")

    summary_str = f"Current Summary:\n{summary.model_dump_json(indent=2)}"

    # Assuming the refine_template has placeholders for summary and feedback
    user_prompt = refine_template.format(
        summary=summary_str,
        feedback=feedback
    )
    return user_prompt

def compose_generate_both_prompt(summary: AnalyseSummary, user: UserInfo) -> Tuple[str, str]:
    """Composes the prompt for generating both resume and cover letter."""
    system_prompt = _read_prompt_template("generate_both_system.md")

    # The user prompt content is constructed based on the available data,
    # as no specific template file is mentioned for this in the spec.
    user_prompt = f"""
Based on the following analysis and user information, generate a resume and a cover letter.

**Analysis Summary:**
{summary.model_dump_json(indent=2)}

**User Information:**
Resume: {user.resume_text}
Projects: {user.projects_text or 'Not provided'}
Extras: {user.extras or 'Not provided'}
"""
    return system_prompt, user_prompt
