from typing import Dict, Any
from . import llm_service

def analyse(jd: str, user_info: str) -> Dict[str, Any]:
    """
    Analyzes the job description and user information.
    """
    if not jd or not user_info:
        raise ValueError("Job Description and User Info cannot be empty.")
    return llm_service.analyse_llm(jd, user_info)

def refine(summary: Dict[str, Any], feedback: str) -> Dict[str, Any]:
    """
    Refines the analysis based on user feedback.
    """
    if not summary or not feedback:
        raise ValueError("Summary and feedback cannot be empty.")
    return llm_service.refine_llm(summary, feedback)
