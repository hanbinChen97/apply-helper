import streamlit as st
import os
import datetime
from services import analyse_service, generation_service, pdf_service

def initialize_session_state():
    """Initializes session state variables."""
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'resume_md' not in st.session_state:
        st.session_state.resume_md = None
    if 'cover_letter_txt' not in st.session_state:
        st.session_state.cover_letter_txt = None
    if 'error' not in st.session_state:
        st.session_state.error = None

def handle_analyse(jd, user_info):
    """Handles the 'Analyse' button click."""
    if not jd or not user_info:
        st.session_state.error = "Job Description and User Info cannot be empty."
        return

    st.session_state.error = None
    with st.spinner("Analyzing and generating documents..."):
        try:
            summary = analyse_service.analyse(jd, user_info)
            st.session_state.summary = summary

            resume_md, cover_letter_txt = generation_service.generate_both(summary, user_info)
            st.session_state.resume_md = resume_md
            st.session_state.cover_letter_txt = cover_letter_txt
        except Exception as e:
            st.session_state.error = f"An error occurred during analysis: {e}"

def handle_refine(feedback):
    """Handles the 'Refine' button click."""
    if not st.session_state.summary:
        st.session_state.error = "You must perform an initial analysis first."
        return
    if not feedback:
        st.session_state.error = "Feedback cannot be empty."
        return

    st.session_state.error = None
    with st.spinner("Refining analysis and re-generating documents..."):
        try:
            # Assume user_info is still available from the text area or stored in session
            user_info = st.session_state.user_info_input

            updated_summary = analyse_service.refine(st.session_state.summary, feedback)
            st.session_state.summary = updated_summary

            resume_md, cover_letter_txt = generation_service.generate_both(updated_summary, user_info)
            st.session_state.resume_md = resume_md
            st.session_state.cover_letter_txt = cover_letter_txt
        except Exception as e:
            st.session_state.error = f"An error occurred during refinement: {e}"

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide")
    st.title("AI-powered Resume & Cover Letter Generator")

    initialize_session_state()

    # --- Sidebar for Inputs and Controls ---
    with st.sidebar:
        st.header("Inputs")
        jd_input = st.text_area("1. Paste Job Description", height=150)
        user_info_input = st.text_area("2. Paste Your Resume/Info", height=200)
        st.session_state.user_info_input = user_info_input # Store for refine

        if st.button("Analyse", use_container_width=True):
            handle_analyse(jd_input, user_info_input)

        st.header("Refine")
        feedback_input = st.text_area("3. Provide Feedback to Refine", height=100)
        if st.button("Refine", use_container_width=True):
            handle_refine(feedback_input)

        st.header("Export")
        if st.button("Export to PDF", use_container_width=True):
            if st.session_state.resume_md and st.session_state.cover_letter_txt:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                resume_path = os.path.join("exports", f"{timestamp}_resume.pdf")
                cover_letter_path = os.path.join("exports", f"{timestamp}_cover_letter.pdf")

                with st.spinner("Generating PDFs..."):
                    try:
                        pdf_service.md_to_pdf(st.session_state.resume_md, resume_path)
                        st.session_state.resume_pdf_path = resume_path

                        pdf_service.txt_to_pdf(st.session_state.cover_letter_txt, cover_letter_path)
                        st.session_state.cover_letter_pdf_path = cover_letter_path
                        st.success("PDFs generated successfully!")
                    except Exception as e:
                        st.error(f"Failed to generate PDFs: {e}")
            else:
                st.warning("Please generate documents before exporting.")

        # Display download buttons if PDFs have been created
        if 'resume_pdf_path' in st.session_state and os.path.exists(st.session_state.resume_pdf_path):
            with open(st.session_state.resume_pdf_path, "rb") as f:
                st.download_button("Download Resume PDF", f, file_name=os.path.basename(st.session_state.resume_pdf_path), use_container_width=True)

        if 'cover_letter_pdf_path' in st.session_state and os.path.exists(st.session_state.cover_letter_pdf_path):
            with open(st.session_state.cover_letter_pdf_path, "rb") as f:
                st.download_button("Download Cover Letter PDF", f, file_name=os.path.basename(st.session_state.cover_letter_pdf_path), use_container_width=True)


    # --- Main Area for Outputs ---
    if st.session_state.error:
        st.error(st.session_state.error)

    if st.session_state.summary:
        st.header("Analysis Summary")
        st.json(st.session_state.summary)

    col1, col2 = st.columns(2)
    with col1:
        st.header("Resume Preview")
        if st.session_state.resume_md:
            st.markdown(st.session_state.resume_md)
        else:
            st.info("Resume will be generated here.")

    with col2:
        st.header("Cover Letter Preview")
        if st.session_state.cover_letter_txt:
            st.text(st.session_state.cover_letter_txt)
        else:
            st.info("Cover Letter will be generated here.")

if __name__ == "__main__":
    main()
