import pytest
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.analyse_service import analyse, refine
from src.core.schemas import JobDescription, UserInfo, AnalyseSummary

@pytest.fixture
def sample_jd():
    return JobDescription(title="Test Job", raw_text="We need a Python developer.")

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

@patch('src.services.analyse_service.chat_complete')
def test_analyse_success(mock_chat_complete, sample_jd, sample_user_info, sample_summary):
    """Tests the analyse function successfully returns a summary."""
    mock_chat_complete.return_value = sample_summary.model_dump()

    result = analyse(sample_jd, sample_user_info)

    assert result == sample_summary
    mock_chat_complete.assert_called_once()

@patch('src.services.analyse_service.chat_complete')
def test_refine_success(mock_chat_complete, sample_summary):
    """Tests the refine function successfully returns a refined summary."""
    refined_summary_data = sample_summary.model_dump()
    refined_summary_data["suggestions"].append("Highlight FastAPI experience")

    mock_chat_complete.return_value = refined_summary_data

    feedback = "Emphasize FastAPI"
    result = refine(sample_summary, feedback)

    assert "Highlight FastAPI experience" in result.suggestions
    mock_chat_complete.assert_called_once()
