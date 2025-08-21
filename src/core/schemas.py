from pydantic import BaseModel
from typing import Optional, List

class JobDescription(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    raw_text: str

class UserInfo(BaseModel):
    resume_text: str
    projects_text: Optional[str] = None
    extras: Optional[str] = None

class AnalyseSummary(BaseModel):
    key_requirements: List[str]
    matched_strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    short_pitch: str

class FinalArtifacts(BaseModel):
    resume_md: str
    cover_letter_txt: str
