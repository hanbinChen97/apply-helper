# 📄 PRD — AI-powered Resume & Cover Letter Generator

## 1. Product Overview

This tool helps users **automatically generate a Resume and Cover Letter** tailored to a given **Job Description (JD)**.

Frontend: **Streamlit** for simple, interactive UI.  
Backend: **Python + LiteLLM** for multi-provider LLM integration.

目标:

* 快速生成个性化简历 & 求职信
* 用户可反复迭代修改，直到满意
* 一键导出 PDF

---

## 2. User Flow

1. **输入阶段**

   * 用户粘贴 **Job Description (JD)**
   * 用户粘贴 **个人信息**（简历内容、项目介绍、其他说明）

2. **分析 & 生成阶段**

   * 点击 **Analyse** → LLM 解析 JD + 用户信息，产出分析总结（关键技能、岗位要求、匹配点、差距、建议、短 Pitch）
   * 随后基于总结触发一次 **生成**：输出 **Resume (Markdown)** 与 **Cover Letter (Text)**
   * UI 在同一屏内立即预览两份文档（无单独“预览阶段”）

3. **Refine 阶段**

   * 用户在 **Feedback InputBox** 输入反馈（例如“强调 CI/CD 和 DevOps”）
   * 点击 **Refine** → 基于反馈更新分析总结，并再次 **生成** 两份文档
   * UI 始终预览最新的 Resume & Cover Letter

4. **导出阶段**

   * 用户点击 **Export PDF**
   * 系统导出 Resume PDF + Cover Letter PDF

---

## 3. Core Features

* **Frontend (Streamlit)**

  * InputBox: Job Description
  * InputBox: User Info
  * Button: **Analyse**
  * InputBox: 用户反馈
  * Button: **Refine**
  * Preview Resume (Markdown) & Cover Letter (Text)
  * Button: **Export PDF**

* **Backend (LLM)**

  * **Analyse Prompt** → 输出 JSON summary
  * **Refine Prompt** → 基于用户反馈更新 summary
  * **Generate Prompt (Single)** → 同时生成 Resume (Markdown) + Cover Letter (Text)

* **Export**

  * Markdown → PDF
  * Text → PDF

---

## 3.1 UI Spec

- **Layout:** 单页 Streamlit；左侧输入与控制，右侧结果与预览。
- **Inputs:**
  - `Job Description` 文本域（必填）
  - `User Info` 文本域（可包含简历要点、项目、加分项）
  - `Feedback` 文本域（可选，用于强调或修正分析方向）
- **Actions:**
  - `Analyse`：解析 JD+User，生成/更新总结；随后立即生成并预览两份文档
  - `Refine`：基于反馈更新总结；随后重新生成并预览两份文档
  - `Export PDF`：导出两份 PDF（Resume、Cover Letter）
- **Outputs:**
  - `Analyse Summary`（关键技能、匹配点、差距、建议、短 Pitch）
  - `Resume (Markdown 渲染预览)`
  - `Cover Letter (纯文本预览)`

---

## 3.2 Button Actions

- **Analyse:**
  - 前置校验：`JD` 和 `User Info` 不为空。
  - 生成总结：`services/analyse_service.analyse(jd, user)`。
  - 生成文档：`services/generation_service.generate_both(summary, user)`。
  - UI 更新：展示 `Analyse Summary` 与两份文档预览。
  - 错误处理：捕获 LLM/解析错误，展示可重试提示；记录结构化日志。

- **Refine:**
  - 前置校验：存在有效 `summary` 且 `Feedback` 非空。
  - 更新总结：`services/analyse_service.refine(summary, feedback)`。
  - 重新生成：`services/generation_service.generate_both(updated_summary, user)`。
  - UI 更新：覆盖预览为最新版本。

- **Export PDF:**
  - 前置校验：已生成 `Resume` 与 `Cover Letter`。
  - 调用 `services/pdf_service.md_to_pdf(resume_md, path)` 与 `txt_to_pdf(cover_letter_txt, path)` 生成两份 PDF。
  - 提供下载：通过 `st.download_button` 返回二者（或打包 zip）。
  - 默认命名：`exports/{timestamp}_resume.pdf` 与 `exports/{timestamp}_cover_letter.pdf`。

---


## 4. 技术实现概览

### 4.1 项目结构

```
apply-helper/
├── pyproject.toml           # 项目依赖与配置
├── README.md                # 项目说明文档
├── app.py                   # Streamlit 前端主入口
├── docs/
│   ├── prd.md               # 产品需求文档
│   └── spec.md              # 技术规格说明
├── services/
│   ├── analyse_service.py   # JD/用户信息分析与总结
│   ├── generation_service.py # 简历与求职信生成
│   ├── pdf_service.py       # PDF 导出功能
│   └── llm_service.py       # LLM/LiteLLM 统一封装与调用
├── llm/
│   ├── litellm_client.py    # LiteLLM API 封装
│   └── prompt_templates.py  # LLM Prompt 模板管理
├── exports/                 # 导出 PDF 文件目录
└── tests/                   # 单元测试
```

### 4.2 主要技术实现

- **前端**：Streamlit 单页应用，左侧输入与控制，右侧结果与预览。
- **后端服务**：
  - `analyse_service.py`：负责 JD/用户信息分析与总结。
  - `generation_service.py`：负责简历与求职信生成。
  - `pdf_service.py`：负责 PDF 导出。
  - `llm_service.py`：统一封装 LLM 调用，底层通过 `llm/litellm_client.py` 对接 LiteLLM。
  - `llm/prompt_templates.py`：管理各类 Prompt 模板。
- **依赖管理**：推荐使用 uv 管理 Python 依赖。
- **LLM 接入**：LiteLLM 支持多云模型，密钥通过 .env 配置。
- **扩展性**：各服务模块解耦，便于未来扩展多语言、社交信息抓取等。

---

## 5. Example Workflow

* 输入 JD: "Looking for a React developer with AI integration experience..."
* 输入 Resume/Project info
* 点击 **Analyse** → 输出关键技能、匹配点、差距，并生成 Resume(MD) + Cover Letter(TXT) 预览
* 用户输入反馈 "强调 CI/CD 和 DevOps"
* 点击 **Refine** → 更新总结并重新生成两份文档（即时预览）
* **导出 PDF**

---

## 6. Future Extensions

* 多语言支持 (EN/DE)
* 自动建议改进点
* GitHub/LinkedIn 自动抓取信息
* ATS 优化模式

---
