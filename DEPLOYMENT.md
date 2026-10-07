# Deployment Checklist

## 1. Local test

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_real_key
```

Start:

```powershell
streamlit run app.py
```

## 2. GitHub

From the project folder:

```powershell
git init
git add .
git commit -m "Initial AI Research Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Before pushing, verify:

```powershell
git status
```

`.env` must NOT appear as a file ready to commit.

## 3. Streamlit Community Cloud

Open Streamlit Community Cloud and choose **Create app**.

Select:

- Repository: your GitHub repository
- Branch: `main`
- Main file path: `app.py`

Open **Advanced settings** and put this in Secrets:

```toml
GROQ_API_KEY = "your_real_groq_api_key"
```

Deploy.

## 4. After deployment

Test:

- A short research topic
- A current topic
- A technical topic
- A topic with statistics

Check that the report contains:

- Title
- Introduction
- Key Findings
- Detailed Analysis
- Important Facts/Data
- Conclusion
- Sources / References

## 5. Security reminder

Never paste the actual API key into:

- GitHub
- README
- Python source
- screenshots
- public messages

If a key is accidentally exposed, revoke/rotate it from Groq immediately.
