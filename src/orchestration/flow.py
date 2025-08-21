from typing import Optional
from src.core.schemas import JobDescription, UserInfo, AnalyseSummary, FinalArtifacts
from src.services import analyse_service, generation_service
from src.core.logger import get_logger

logger = get_logger(__name__)

class OrchestrationFlow:
    """
    Manages the state and flow of the resume generation process.
    """
    def __init__(self):
        self.job_description: Optional[JobDescription] = None
        self.user_info: Optional[UserInfo] = None
        self.analysis_summary: Optional[AnalyseSummary] = None
        self.final_artifacts: Optional[FinalArtifacts] = None
        logger.info("OrchestrationFlow initialized.")

    def start_analyse(self, jd: JobDescription, user: UserInfo) -> AnalyseSummary:
        """
        Starts the analysis process and stores the state.
        """
        logger.info("Starting analysis flow.")
        self.job_description = jd
        self.user_info = user

        self.analysis_summary = analyse_service.analyse(jd, user)
        logger.info("Analysis complete.")
        return self.analysis_summary

    def apply_feedback(self, feedback: str) -> AnalyseSummary:
        """
        Applies user feedback to refine the analysis summary.
        Requires analysis_summary to be present.
        """
        if not self.analysis_summary:
            logger.error("Attempted to apply feedback before analysis was complete.")
            raise ValueError("Analysis must be performed before applying feedback.")

        logger.info("Applying user feedback to analysis.")
        self.analysis_summary = analyse_service.refine(self.analysis_summary, feedback)
        logger.info("Refinement complete.")
        return self.analysis_summary

    def finalize_and_generate(self) -> FinalArtifacts:
        """
        Finalizes the process and generates the resume and cover letter.
        Requires analysis_summary and user_info to be present.
        """
        if not self.analysis_summary or not self.user_info:
            logger.error("Attempted to generate artifacts before analysis was complete.")
            raise ValueError("Analysis must be complete before generating artifacts.")

        logger.info("Finalizing and generating artifacts.")
        self.final_artifacts = generation_service.generate_both(self.analysis_summary, self.user_info)
        logger.info("Artifact generation complete.")
        return self.final_artifacts
