"""
Manages all prompt templates for the application.
"""

PROMPT_TEMPLATES = {
    "analyse": """
You are a professional career coach. Analyze the provided Job Description (JD) and User Information.
Your goal is to extract key skills, identify matches and gaps, and provide actionable suggestions.

**Job Description:**
{jd}

**User Information:**
{user}

**Your analysis should be in the following JSON format:**
{{
    "key_skills": ["skill1", "skill2", ...],
    "match_points": ["point1", "point2", ...],
    "gap_points": ["point1", "point2", ...],
    "suggestions": ["suggestion1", "suggestion2", ...],
    "pitch": "A short, compelling pitch for the user."
}}
""",
    "refine": """
You are a professional career coach. A summary has been generated based on a Job Description and User Information.
Now, refine this summary based on the user's feedback.

**Original Summary:**
{summary}

**User Feedback:**
{feedback}

**Your refined analysis should be in the same JSON format as the original:**
{{
    "key_skills": ["skill1", "skill2", ...],
    "match_points": ["point1", "point2", ...],
    "gap_points": ["point1", "point2", ...],
    "suggestions": ["suggestion1", "suggestion2", ...],
    "pitch": "A short, compelling pitch for the user."
}}
""",
    "generate_resume": """
You are a professional resume writer. Based on the following analysis and user information, generate a professional resume in Markdown format.
The resume should be tailored to the job description implied in the analysis.

**Analysis Summary:**
{summary}

**User Information:**
{user}

**Instructions:**
- The output must be a single block of Markdown.
- Highlight the most relevant skills and experiences.
- Use professional and action-oriented language.
- Do not include any introductory text like "Here is the resume:".
""",
    "generate_cover_letter": """
You are a professional cover letter writer. Based on the following analysis and user information, generate a compelling cover letter.
The cover letter should be tailored to the job description implied in the analysis.

**Analysis Summary:**
{summary}

**User Information:**
{user}

**Instructions:**
- The output must be plain text.
- The tone should be professional and enthusiastic.
- Address the key requirements from the job description.
- Do not include any introductory text like "Here is the cover letter:".
"""
}

def get_template(name: str) -> str:
    """
    Retrieves a prompt template by name.
    """
    template = PROMPT_TEMPLATES.get(name)
    if not template:
        raise ValueError(f"Template '{name}' not found.")
    return template
