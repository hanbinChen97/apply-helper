# 📑 技术规格说明（SPR） — AI-powered Resume & Cover Letter Generator

## 1. 项目结构

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
│       ├── pdf_service.py          # PDF 导出功能
│       └── llm_service.py          # LLM/LiteLLM 统一封装与调用
│   └── llm/
│       ├── litellm_client.py       # LiteLLM API 封装
│       └── prompt_templates.py     # LLM Prompt 模板管理
├── exports/                 # 导出 PDF 文件目录
└── tests/                   # 单元测试
```

## 2. 主要 Python 文件与函数

### 2.1 `app/ui.py` — Streamlit 前端主入口

- 页面布局：左侧输入与控制，右侧结果与预览
- 主要函数：
	- `main()`：应用入口，负责 UI 渲染与交互逻辑
	- `render_inputs()`：输入区（JD、用户信息、反馈）
	- `render_outputs()`：输出区（分析总结、简历预览、求职信预览）
	- `handle_analyse()`：分析按钮回调，调用分析与生成服务
	- `handle_refine()`：反馈按钮回调，调用 refine 与生成服务
	- `handle_export()`：导出 PDF 按钮回调



### 2.2 LLM 相关代码

- `app/services/llm_service.py`：统一封装 LLM 调用逻辑，负责模型选择、异常处理、日志记录。
- `app/llm/litellm_client.py`：LiteLLM API 封装，负责与 OpenAI/Azure/Gemini 等模型的底层交互。
- `app/llm/prompt_templates.py`：管理分析、生成、优化等各类 Prompt 模板。

#### 主要接口伪代码示例

```python
# llm_service.py
from app.llm.litellm_client import call_llm
from app.llm.prompt_templates import get_template

def analyse_llm(jd: str, user: str) -> dict:
	prompt = get_template("analyse").format(jd=jd, user=user)
	result = call_llm(prompt)
	return parse_summary(result)

def refine_llm(summary: dict, feedback: str) -> dict:
	prompt = get_template("refine").format(summary=summary, feedback=feedback)
	result = call_llm(prompt)
	return parse_summary(result)

# litellm_client.py
import litellm
def call_llm(prompt: str) -> str:
	response = litellm.completion(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
	return response["choices"][0]["message"]["content"]
```


### 2.3 业务服务

- `app/services/analyse_service.py`
	```python
	def analyse(jd: str, user: str) -> dict:
			return llm_service.analyse_llm(jd, user)

	def refine(summary: dict, feedback: str) -> dict:
			return llm_service.refine_llm(summary, feedback)
	```

- `app/services/generation_service.py`
	```python
	def generate_both(summary: dict, user: str) -> Tuple[str, str]:
			resume_md = llm_service.generate_resume(summary, user)
			cover_txt = llm_service.generate_cover_letter(summary, user)
			return resume_md, cover_txt
	```

- `app/services/pdf_service.py`
	```python
	def md_to_pdf(md: str, path: str) -> None:
			# 使用 weasyprint 或 pdfkit 实现
			pass

	def txt_to_pdf(txt: str, path: str) -> None:
			# 使用 weasyprint 或 pdfkit 实现
			pass
	```

## 3. Streamlit UI 设计

### 3.1 页面布局

- **左栏（Sidebar）**：
	- Job Description 输入框（必填）
	- User Info 输入框（必填）
	- Feedback 输入框（可选）
	- Analyse 按钮
	- Refine 按钮
	- Export PDF 按钮

- **主区（Main Area）**：
	- Analyse Summary（结构化展示：关键技能、匹配点、差距、建议、Pitch）
	- Resume 预览（Markdown 渲染）
	- Cover Letter 预览（纯文本）
	- 导出 PDF 下载按钮（支持打包下载）

### 3.2 交互逻辑

- **Analyse**：校验输入，调用 `analyse_service.analyse`，随后 `generation_service.generate_both`，更新预览区
- **Refine**：校验 summary 与反馈，调用 `analyse_service.refine`，随后 `generation_service.generate_both`，更新预览区
- **Export PDF**：校验已生成文档，调用 `pdf_service.md_to_pdf` 与 `txt_to_pdf`，提供下载

### 3.3 错误处理与日志

- 所有服务调用异常均捕获，UI 友好提示，结构化日志记录


## 4. 依赖管理与扩展

### 4.1 依赖管理（uv 推荐）

- 项目依赖通过 `pyproject.toml` 管理，推荐使用 [uv](https://github.com/astral-sh/uv) 进行安装和运行。
- 安装 uv：
	```sh
	pip install uv
	```
- 安装依赖：
	```sh
	uv sync
	```
- 启动应用：
	```sh
	uv run start
	# 或
	uv run streamlit run app/ui.py
	```

### 4.2 LLM 接入（LiteLLM 指南）

- LLM 服务通过 [LiteLLM](https://github.com/BerriAI/litellm) 统一接入，支持 OpenAI、Azure、Gemini 等主流模型。
- 配置密钥：
	- 复制 `.env.example` 为 `.env`，填写 `OPENAI_API_KEY` 或其他云厂商密钥。
- 主要用法：
	- 在 `analyse_service.py`、`generation_service.py` 中通过 LiteLLM 调用 LLM API。
	- 推荐使用 Pydantic 进行输入/输出数据结构校验。
- 参考代码片段：
	```python
	import litellm
	response = litellm.completion(
			model="gpt-3.5-turbo",
			messages=[{"role": "user", "content": prompt}],
			api_key="你的API密钥"
	)
	# 解析 response['choices'][0]['message']['content']
	```

### 4.3 PDF 导出

- 推荐使用 WeasyPrint 或 pdfkit 实现 Markdown/Text 到 PDF 的转换。

### 4.4 未来扩展

- 多语言支持、自动建议、社交信息抓取、ATS 优化等。

---
