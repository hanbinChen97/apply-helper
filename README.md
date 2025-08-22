# AI Resume & Cover Letter Generator

AI-powered app that analyzes a job description and your background, then generates a tailored resume (Markdown → PDF) and cover letter (text → PDF). Built with Streamlit, Pydantic, and LiteLLM.

## Features
- Analyse JD + resume to extract strengths, gaps, and suggestions
- Refine analysis with feedback
- Generate resume (Markdown) and cover letter (text)
- Export PDFs and a combined ZIP

## Quick Start
1) Prereqs: Python 3.9+, and either `uv` (recommended) or `pip`.
2) Configure secrets: copy `.env.example` → `.env` and set API keys (`OPENAI_API_KEY`, or Azure/Gemini keys).
3) Install deps:
   - Using uv: `uv sync`
4) Run the app:
   - `uv run start` (or `uv run streamlit run app.py`)
   - Open the URL printed by Streamlit (typically http://localhost:8501).

## Project Structure

