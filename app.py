import streamlit as st
import tempfile
from pathlib import Path
import zipfile

# Make sure the root of the project is in the Python path
import sys
sys.path.append(str(Path(__file__).parent))

# Import our project modules
from src.orchestration.flow import OrchestrationFlow
from src.core.schemas import JobDescription, UserInfo
from src.services.pdf_service import md_to_pdf, txt_to_pdf

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume & Cover Letter Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- State Management ---
# Initialize the orchestration flow in the session state if it doesn't exist.
if 'flow' not in st.session_state:
    st.session_state.flow = OrchestrationFlow()

# Initialize a stage manager for the UI view.
if 'stage' not in st.session_state:
    st.session_state.stage = 'input'

# --- Helper Functions ---
def go_to_stage(stage_name):
    """Callback to change the UI stage."""
    st.session_state.stage = stage_name

def handle_analysis():
    """Callback for the 'Analyse' button."""
    jd_text = st.session_state.get("jd_text", "")
    user_info_text = st.session_state.get("user_info_text", "")

    if not jd_text or not user_info_text:
        st.sidebar.error("Please provide both a Job Description and your information.")
        return

    jd = JobDescription(title="Job", raw_text=jd_text)
    user = UserInfo(resume_text=user_info_text)

    with st.spinner("Analyzing... This may take a moment."):
        try:
            st.session_state.flow.start_analyse(jd, user)
            go_to_stage('analysis')
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")

def handle_refinement():
    """Callback for the 'Refine Analysis' button."""
    feedback = st.session_state.get("feedback_text", "")
    if not feedback:
        st.warning("Please provide feedback to refine the analysis.")
        return
    with st.spinner("Refining analysis..."):
        try:
            st.session_state.flow.apply_feedback(feedback)
        except Exception as e:
            st.error(f"An error occurred during refinement: {e}")

def handle_generation():
    """Callback for the 'Next: Generate' button."""
    with st.spinner("Generating your documents..."):
        try:
            st.session_state.flow.finalize_and_generate()
            go_to_stage('done')
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")

def create_download_zip():
    """Creates a zip file with the generated PDFs and returns its bytes."""
    artifacts = st.session_state.flow.final_artifacts
    if not artifacts:
        return None

    # Create a temporary directory to store the files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        resume_path = temp_path / "resume.pdf"
        cover_letter_path = temp_path / "cover_letter.pdf"
        zip_path = temp_path / "resume_and_cover_letter.zip"

        # Generate PDFs
        md_to_pdf(artifacts.resume_md, resume_path)
        txt_to_pdf(artifacts.cover_letter_txt, cover_letter_path)

        # Create a zip file
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(resume_path, arcname="resume.pdf")
            zipf.write(cover_letter_path, arcname="cover_letter.pdf")

        # Read the zip file into memory to be returned
        with open(zip_path, 'rb') as f:
            return f.read()

# --- UI Rendering ---
st.title("📄 AI-powered Resume & Cover Letter Generator")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("1. Your Information")
    st.text_area("Paste the Job Description here", height=200, key="jd_text")
    st.text_area("Paste your resume, project details, etc.", height=300, key="user_info_text")

    st.button("Analyse", on_click=handle_analysis, use_container_width=True)

# --- Main Content Area based on Stage ---
if st.session_state.stage == 'input':
    st.info("Please fill in the details in the sidebar and click 'Analyse' to start.")

elif st.session_state.stage == 'analysis':
    st.header("2. Analysis & Refinement")
    summary = st.session_state.flow.analysis_summary
    if summary:
        st.write(f"**Short Pitch:** {summary.short_pitch}")

        col1, col2 = st.columns(2)
        with col1:
            st.success("**✅ Matched Strengths**")
            for item in summary.matched_strengths:
                st.write(f"- {item}")

        with col2:
            st.warning("**⚠️ Gaps**")
            for item in summary.gaps:
                st.write(f"- {item}")

        st.info("**💡 Suggestions for Improvement**")
        for item in summary.suggestions:
            st.write(f"- {item}")

        st.markdown("---")
        st.subheader("Refine Analysis")
        st.text_area("Provide feedback to improve the analysis (e.g., 'Emphasize my experience with DevOps'). Press the button to apply.", key="feedback_text")
        st.button("Refine Analysis", on_click=handle_refinement, use_container_width=True)

        st.markdown("---")
        st.header("3. Generate Documents")
        st.button("Next: Generate Resume & Cover Letter", on_click=handle_generation, type="primary", use_container_width=True)

elif st.session_state.stage == 'done':
    st.header("4. Your Generated Documents")
    artifacts = st.session_state.flow.final_artifacts
    if artifacts:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Resume (Markdown)")
            st.markdown(artifacts.resume_md)

        with col2:
            st.subheader("Cover Letter")
            st.text(artifacts.cover_letter_txt)

        st.markdown("---")
        st.header("5. Export")

        zip_bytes = create_download_zip()
        if zip_bytes:
            st.download_button(
                label="Export PDFs (as .zip)",
                data=zip_bytes,
                file_name="resume_and_cover_letter.zip",
                mime="application/zip",
                use_container_width=True
            )
    else:
        st.error("Something went wrong. No documents were generated.")

    if st.button("Start Over", use_container_width=True):
        # Reset the flow and go back to the input stage
        st.session_state.flow = OrchestrationFlow()
        go_to_stage('input')
