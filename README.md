# AI Resume & Cover Letter Generator

AI-powered app that analyzes a job description and your background, then generates a tailored resume (Markdown → PDF) and cover letter (text → PDF). Built with Streamlit, Pydantic, and LiteLLM.

## Features
- Analyse JD + resume to extract strengths, gaps, and suggestions
- Refine analysis with feedback
- Generate resume (Markdown) and cover letter (text)
- Export PDFs and a combined ZIP

## Quick Start

### 1. Configure Secrets
First, copy the example environment file and add your LLM API key.

```bash
cp .env.example .env
```
Now, edit the `.env` file to add your `OPENAI_API_KEY` or keys for other supported providers.

### 2. Install Dependencies
You will need Python 3.9+ and can use `uv` (recommended) or `pip`.

**Using uv:**
```bash
# Install uv if you don't have it
pip install uv

# Install dependencies from pyproject.toml
uv sync
```

**Using pip:**
```bash
pip install streamlit litellm pydantic pyyaml weasyprint python-dotenv pytest tenacity markdown-it-py
```
*Note: `weasyprint` may require installing system-level dependencies like Pango, Cairo, and GDK-PixBuf. Please see the [WeasyPrint documentation](https://doc.weasyprint.org/stable/first_steps.html#installation) for platform-specific instructions.*

### 3. Run the Application
Once dependencies are installed, run the Streamlit app:

**Using uv:**
The `start` script in `pyproject.toml` runs the app for you.
```bash
uv run start
```

**Using streamlit directly:**
```bash
streamlit run app/ui.py
```
You can now view the application in your browser, typically at `http://localhost:8501`.

## Project Structure
```
apply-helper/
├── pyproject.toml           # Project dependencies and scripts
├── README.md                # This file
├── docs/
│   ├── prd.md               # Product Requirements Document
│   └── spec.md              # Technical Specifications
├── app/
│   ├── ui.py                # Streamlit frontend main entry point
│   ├── services/
│   │   ├── analyse_service.py
│   │   ├── generation_service.py
│   │   ├── pdf_service.py
│   │   └── llm_service.py
│   └── llm/
│       ├── litellm_client.py
│       └── prompt_templates.py
├── exports/                 # Directory for exported PDF files
└── tests/                   # Unit tests
```