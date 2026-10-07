# 🔎 AI Research Agent

A simple, beginner-friendly AI Research Agent built with **CrewAI, Groq,
DuckDuckGo, and Streamlit**.

## What it does

1. User enters a research topic.
2. One CrewAI agent receives the topic.
3. The agent uses DuckDuckGo web search.
4. The agent analyzes the gathered information with Groq.
5. A structured Markdown research report is generated.
6. Streamlit displays the report and provides a Markdown download.

## Architecture

```text
User Topic
    ↓
Streamlit
    ↓
One CrewAI Research Agent
    ↓
DuckDuckGo Web Search
    ↓
Groq GPT-OSS 120B
    ↓
Research + Analysis
    ↓
Structured Report
    ↓
Streamlit
```

This project intentionally uses **one agent only**. There is no database,
authentication, custom backend, or unnecessary infrastructure.

## Project structure

```text
ai-research-agent/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### `app.py`
The complete Streamlit application, CrewAI agent, task, DuckDuckGo tool,
Groq configuration, error handling, and report display.

### `requirements.txt`
Pinned dependencies used by this project.

### `.env.example`
Safe template showing the required local environment variable.

### `.gitignore`
Prevents `.env` and Streamlit secrets from being committed.

## Current package approach

This project targets Python 3.12.

The pinned CrewAI release is `1.15.23`. CrewAI 1.15.x supports Python
3.10 through 3.13. Groq's API is OpenAI-compatible, so the app uses
CrewAI's current `custom_openai=True` configuration with Groq's OpenAI
compatible endpoint. This avoids relying on the older LiteLLM-based Groq
configuration.

The requested Groq model is:

```text
openai/gpt-oss-120b
```

DuckDuckGo search uses the current `ddgs` package.

## Local Windows setup

Open PowerShell in the project folder:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_real_groq_api_key
```

Run:

```powershell
streamlit run app.py
```

## GitHub security

**Never commit `.env`.**

The real key must never appear in:

- `app.py`
- `README.md`
- GitHub
- screenshots
- public code

The `.gitignore` already excludes `.env` and `.streamlit/secrets.toml`.

## Streamlit Community Cloud deployment

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select your GitHub repository.
5. Select the branch, normally `main`.
6. Set the main file to:

```text
app.py
```

7. Open **Advanced settings**.
8. In **Secrets**, enter:

```toml
GROQ_API_KEY = "your_real_groq_api_key"
```

9. Save/deploy the app.

Do **not** upload `.env` to GitHub.

## Example topics

Try:

- Impact of Artificial Intelligence on Education
- Renewable Energy Trends in 2026
- Cybersecurity Challenges in Small Businesses
- Generative AI in Software Development
- Benefits and Risks of Autonomous Vehicles
- Artificial Intelligence in Healthcare
- Cloud Computing Security
- Future of Remote Work

## Important limitation

DuckDuckGo search is a free web-search layer and search results can vary.
The report should be treated as an AI-assisted research draft: verify
important claims and sources before using it for academic, legal, medical,
financial, or other high-stakes decisions.

## Troubleshooting

### `GROQ_API_KEY is missing`
Local: make sure `.env` exists and contains the key.

Cloud: make sure `GROQ_API_KEY` is present in Streamlit's Secrets settings.

### Groq authentication error
Check that the Groq API key is valid and active.

### CrewAI import error
Delete `.venv`, recreate it with Python 3.12, and reinstall:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Search error
DuckDuckGo can temporarily rate-limit or fail to return results. Try the
research again later or use a more specific topic.

### Streamlit deployment error
Check the deployment logs and confirm that:

- `requirements.txt` is in the repository root.
- `app.py` is in the repository root.
- Python 3.12 is selected.
- `GROQ_API_KEY` is configured in Secrets.

## License

This project is intended as a beginner-friendly educational AI application.
