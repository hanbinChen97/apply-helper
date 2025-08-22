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
```
apply-helper/
├── pyproject.toml           # 项目依赖与配置
├── README.md                # 项目说明文档
├── docs/
│   ├── prd.md               # 产品需求文档
│   └── spec.md              # 技术规格说明（本文件）
├── app/
│   ├── ui.py                # Streamlit 前端主入口
│   └── services/
│       ├── analyse_service.py      # JD/用户信息分析与总结
│       ├── generation_service.py   # 简历与求职信生成
│       └── pdf_service.py          # PDF 导出功能
├── exports/                 # 导出 PDF 文件目录
└── tests/                   # 单元测试
```