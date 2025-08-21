from src.core.schemas import JobDescription, UserInfo, AnalyseSummary
from src.llm.client import chat_complete
from src.llm.prompts import compose_analyse_prompt, compose_refine_prompt
from src.core.logger import get_logger

logger = get_logger(__name__)

def analyse(jd: JobDescription, user: UserInfo) -> AnalyseSummary:
    """
    Analyzes the job description and user info to produce a summary.
    """
    logger.info("Starting analysis of job description and user info.")
    system_prompt, user_prompt = compose_analyse_prompt(jd, user)

    response_dict = chat_complete(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
        response_format="json"
    )

    if not isinstance(response_dict, dict):
        raise TypeError(f"Expected a dictionary response, but got {type(response_dict)}")

    return AnalyseSummary(**response_dict)

def refine(summary: AnalyseSummary, feedback: str) -> AnalyseSummary:
    """
    Refines an existing analysis summary based on user feedback.
    """
    logger.info("Refining analysis based on user feedback.")
    user_prompt = compose_refine_prompt(summary, feedback)

    system_prompt = "You are a career assistant. Refine the provided analysis based on the user's feedback. Output JSON."

    response_dict = chat_complete(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
        response_format="json"
    )

    if not isinstance(response_dict, dict):
        raise TypeError(f"Expected a dictionary response, but got {type(response_dict)}")

    return AnalyseSummary(**response_dict)
