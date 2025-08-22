from typing import Tuple, Dict, Any
from app.services import llm_service

def generate_both(summary: Dict[str, Any], user_info: str) -> Tuple[str, str]:
    """
    Generates both the resume (Markdown) and cover letter (text).
    """
    if not summary:
        raise ValueError("Analysis summary cannot be empty.")

    resume_md = llm_service.generate_resume_llm(summary, user_info)
    cover_letter_txt = llm_service.generate_cover_letter_llm(summary, user_info)

    return resume_md, cover_letter_txt
