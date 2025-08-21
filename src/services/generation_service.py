from src.core.schemas import UserInfo, AnalyseSummary, FinalArtifacts
from src.llm.client import chat_complete
from src.llm.prompts import compose_generate_both_prompt
from src.core.logger import get_logger

logger = get_logger(__name__)

def generate_both(summary: AnalyseSummary, user: UserInfo) -> FinalArtifacts:
    """
    Generates both a resume and a cover letter from the analysis summary and user info.
    """
    logger.info("Generating resume and cover letter.")
    system_prompt, user_prompt = compose_generate_both_prompt(summary, user)

    response_dict = chat_complete(
        messages=[{"role": "user", "content": user_prompt}],
        system_prompt=system_prompt,
        response_format="json"
    )

    if not isinstance(response_dict, dict):
        raise TypeError(f"Expected a dictionary response, but got {type(response_dict)}")

    return FinalArtifacts(**response_dict)
