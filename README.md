# 🧠 AI Spreadsheet Analyst — Dashboards & Executive Reports

An AI agent that reads spreadsheets in multiple formats and automatically produces an **interactive dashboard** and an **executive report with business insights**, which can be downloaded as a **PDF**.

Built with **FastAPI**, **Agno**, and **Google Gemini**, with a lightweight dark-themed web front end. Dependencies are managed with **[uv](https://docs.astral.sh/uv/)**.

---

## ✨ Features

- 📂 **Multi-format input** — upload `.csv`, `.tsv`, `.xlsx`, or `.xls` files, or import a public **Google Sheets** link.
- 🤖 **AI-generated insights** — an Agno agent powered by Gemini analyzes statistics and sample rows, then writes a concise executive report in Markdown.
- 📊 **Auto-generated dashboard** — a complete, responsive HTML dashboard (Tailwind CSS + Chart.js) with KPI cards and dynamic charts tailored to your data.
- 📄 **PDF export** — download the executive report as a PDF; the dashboard can also be downloaded as standalone HTML or opened in a new tab.
- 💬 **Natural-language questions** — ask things like *"Which product has the highest margin?"* or *"Identify outliers"* and get instant local answers.
- 🔍 **Built-in data exploration** — KPIs, outlier detection (IQR 1.5×), grouped charts (sum / mean / median), and a sortable preview table.
- 🔁 **Model fallback** — if one Gemini model fails, the API automatically retries with the next one in the list.

---

## 🏗️ Architecture

```
┌────────────────────┐   upload file    ┌──────────────────────┐   prompt    ┌──────────────┐
│  index.html (UI)   │ ───────────────► │  FastAPI (main.py)   │ ──────────► │ Agno Agent   │
│  Tailwind + Chart  │                  │  /api/generate-...   │             │ (agent.py)   │
│  Local analysis    │ ◄─────────────── │  model fallback loop │ ◄────────── │ Gemini LLM   │
└────────────────────┘  report + HTML   └──────────────────────┘  JSON out   └──────────────┘
```

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI server exposing the generation endpoint, CORS, and model fallback logic |
| `agent.py` | Agno agent definition and spreadsheet parsing/summarization helpers |
| `index.html` | Single-page front end: upload, local analysis, AI generation, PDF export |
| `pyproject.toml` | Project metadata and dependencies managed by `uv` |
| `.env` | Environment variables (API key) — **never commit this file** |

---

## 📋 Requirements

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** package manager
- A **Google Gemini API key** — get one at [Google AI Studio](https://aistudio.google.com/apikey)

Install uv if you don't have it yet:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-user>/<your-repo>.git
cd <your-repo>
```

### 2. Set up the project with uv

If the project already has a `pyproject.toml`, just sync the environment:

```bash
uv sync
```

Starting from scratch? Initialize and add the dependencies:

```bash
uv init
uv add fastapi "uvicorn[standard]" agno google-genai pandas openpyxl xlrd python-dotenv python-multipart
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Start the backend

```bash
uv run python main.py
```

Or, with auto-reload via Uvicorn:

```bash
uv run uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` (interactive docs at `/docs`).

### 5. Open the front end

Serve `index.html` with any static server (recommended, to avoid browser restrictions):

```bash
uv run python -m http.server 5500
```

Then open **http://localhost:5500** in your browser. The sidebar shows **"IA Conectada"** when the backend is reachable.

---

## 🧭 How to Use

1. Go to **Análise de Planilhas** (Spreadsheet Analysis).
2. Drag & drop a file, paste a Google Sheets link, or click **"Usar dados de exemplo"** to try the demo dataset.
3. Explore the data locally: ask questions, switch chart types, or sort the preview.
4. Click **"Gerar com IA"** to generate the executive report and interactive dashboard.
5. Download the report as **PDF**, or open/download the dashboard as **HTML**.
6. Check **Visão Geral** (Overview) for consolidated KPIs and proactive insights.

> **Google Sheets tip:** the sheet must be shared as *"Anyone with the link"*.

---

## 🔌 API Reference

### `POST /api/generate-from-file`

Uploads a spreadsheet and returns an AI-generated report and dashboard.

**Request** — `multipart/form-data`

| Field | Type | Description |
| --- | --- | --- |
| `file` | file | `.csv`, `.xls`, or `.xlsx` spreadsheet |

**Response** — `200 OK`

```json
{
  "result": {
    "report": "# Executive Report\n...",
    "html_dashboard": "<!DOCTYPE html>..."
  }
}
```

**Errors** — `500` if every configured model fails (the last error is included in `detail`).

Example with `curl`:

```bash
curl -X POST http://localhost:8000/api/generate-from-file \
  -F "file=@sales.xlsx"
```

---

## ⚙️ Configuration

| Setting | Location | Description |
| --- | --- | --- |
| `GOOGLE_API_KEY` | `.env` | Gemini API credentials |
| `MODELS_TO_TRY` | `main.py` | Ordered list of Gemini models used for fallback |
| `API_URL` | `index.html` | Backend URL used by the front end (default `http://localhost:8000`) |
| `allow_origins` | `main.py` | CORS policy — restrict it in production |

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn, Pandas
- **AI:** Agno agent framework, Google Gemini
- **Frontend:** HTML, Tailwind CSS, Chart.js, SheetJS, Marked, DOMPurify
- **Tooling:** uv (dependency & environment management)

---

## 🔒 Security Notes

- Never commit your `.env` file — add it to `.gitignore`.
- The generated dashboard is rendered inside a **sandboxed iframe** (`allow-scripts` only), and Markdown is sanitized with DOMPurify.
- Tighten the CORS settings (`allow_origins=["*"]`) before deploying to production.
- Spreadsheet summaries (columns, statistics, and a 10-row sample) are sent to the Gemini API — avoid uploading sensitive data you don't want to share with the provider.

---

## 🗺️ Roadmap

- [ ] Support for multi-sheet Excel selection
- [ ] Server-side PDF generation
- [ ] Streaming responses for faster feedback
- [ ] Authentication and per-user history
- [ ] Docker image

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
