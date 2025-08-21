import pytest
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.generation_service import generate_both
from src.core.schemas import UserInfo, AnalyseSummary, FinalArtifacts

@pytest.fixture
def sample_user_info():
    return UserInfo(resume_text="I am a Python developer.")

@pytest.fixture
def sample_summary():
    return AnalyseSummary(
        key_requirements=["Python"],
        matched_strengths=["Python developer"],
        gaps=[],
        suggestions=["Add more projects"],
        short_pitch="A good fit."
    )

@pytest.fixture
def sample_artifacts():
    return FinalArtifacts(
        resume_md="# Resume\n\nThis is my resume.",
        cover_letter_txt="Dear Sir/Madam,\n\nThis is my cover letter."
    )

@patch('src.services.generation_service.chat_complete')
def test_generate_both_success(mock_chat_complete, sample_summary, sample_user_info, sample_artifacts):
    """Tests that generate_both successfully returns artifacts."""
    mock_chat_complete.return_value = sample_artifacts.model_dump()

    result = generate_both(sample_summary, sample_user_info)

    assert result == sample_artifacts
    mock_chat_complete.assert_called_once()
