import os

import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Task
from crewai.tools import tool
from ddgs import DDGS

import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

# Load local .env when running on your computer
load_dotenv()


# ----------------------------
# Streamlit configuration
# ----------------------------

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
)


# ----------------------------
# Custom styling (UI only)
# ----------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=Source+Serif+4:wght@400;600&display=swap');

:root {
    --ink: #14183A;
    --panel: #1C2150;
    --line: #2E3570;
    --text: #E8EAFB;
    --muted: #9AA0D0;
    --aqua: #4FE3C1;
    --amber: #FFB86B;
}

/* App background */
.stApp {
    background:
        radial-gradient(900px 500px at 85% -10%, rgba(79, 227, 193, 0.14), transparent 60%),
        radial-gradient(700px 420px at 0% 0%, rgba(255, 184, 107, 0.08), transparent 60%),
        var(--ink);
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
    height: 0;
}

.block-container {
    max-width: 1000px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Hero */
.hero {
    padding: 1.2rem 0 0.4rem 0;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 0 0 0.9rem 0;
    color: var(--text);
}
.hero h1 .glow {
    background: linear-gradient(90deg, var(--aqua), var(--amber));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    max-width: 60ch;
    line-height: 1.6;
    margin: 0;
}

/* Tech pills */
.pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1.2rem 0 0.5rem 0;
}
.pill {
    border: 1px solid var(--line);
    background: rgba(28, 33, 80, 0.7);
    color: var(--text);
    font-size: 0.82rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}
.pill b {
    color: var(--aqua);
    font-weight: 600;
}

/* Input */
.stTextArea label p {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    font-size: 1rem;
    color: var(--text);
}
.stTextArea textarea {
    background: var(--panel) !important;
    color: var(--text) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    padding: 1rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--aqua) !important;
    box-shadow: 0 0 0 3px rgba(79, 227, 193, 0.18) !important;
}
.stTextArea textarea::placeholder {
    color: #6C73AE !important;
}

/* Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--aqua), #35B8E8);
    color: #0E1230;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(79, 227, 193, 0.28);
    color: #0E1230;
}
.stButton > button[kind="primary"]:focus-visible {
    outline: 2px solid var(--amber);
    outline-offset: 2px;
}
.stDownloadButton > button {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--line);
    border-radius: 12px;
    font-weight: 500;
    transition: border-color 0.15s ease, color 0.15s ease;
}
.stDownloadButton > button:hover {
    border-color: var(--aqua);
    color: var(--aqua);
}

/* Report card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--panel);
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    padding: 0.6rem 1.2rem;
}
.report-head {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    margin: 0.2rem 0 0.2rem 0;
}
.report-meta {
    color: var(--muted);
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
}

/* Report typography */
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown {
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 1.05rem;
    line-height: 1.75;
    color: #DCDFF7;
}
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h1,
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h2,
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
    letter-spacing: -0.01em;
}
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown h2 {
    border-bottom: 1px solid var(--line);
    padding-bottom: 0.35rem;
    margin-top: 1.6rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown a {
    color: var(--aqua);
}

/* Divider + caption */
hr {
    border-color: var(--line) !important;
    opacity: 0.6;
}
.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
    text-align: center;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------
# Model configuration
# ----------------------------

MODEL_NAME = "groq/openai/gpt-oss-120b"


# ----------------------------
# Get Groq API key
# ----------------------------

def get_groq_api_key():
    """Read the API key from Streamlit Secrets first, then .env/environment."""

    try:
        secret_key = st.secrets.get("GROQ_API_KEY")

        if secret_key:
            return secret_key

    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


# ----------------------------
# Web search tool
# ----------------------------

@tool("DuckDuckGo Web Search")
def web_search(query: str) -> str:
    """Search the web with DuckDuckGo and return useful titles, snippets, and URLs."""

    try:
        results = DDGS().text(
            query,
            max_results=6,
        )

        if not results:
            return "No useful search results were found."

        formatted_results = []

        for index, result in enumerate(results, start=1):

            title = result.get(
                "title",
                "Untitled",
            )

            snippet = result.get(
                "body",
                "No snippet available.",
            )

            url = result.get(
                "href",
                "",
            )

            formatted_results.append(
                f"{index}. {title}\n"
                f"   Summary: {snippet}\n"
                f"   URL: {url}"
            )

        return "\n\n".join(formatted_results)

    except Exception as error:

        return f"Web search failed: {error}"


# ----------------------------
# Create research crew
# ----------------------------

def create_research_crew(api_key: str, topic: str):
    """Create the CrewAI research workflow."""

    # Groq model through CrewAI's Groq provider
    llm = LLM(
    model=MODEL_NAME,
    api_key=api_key,
    temperature=0.2,
    max_tokens=5000,
    drop_params=True,
)

    researcher = Agent(
        role="AI Research Specialist",

        goal=(
            "Research the user's topic using web search, evaluate the information, "
            "and produce a clear, accurate, well-structured research report."
        ),

        backstory=(
            "You are a careful research specialist. You search the web before "
            "writing, prefer credible and recent sources, compare information "
            "when possible, and never invent citations or facts."
        ),

        tools=[web_search],

        llm=llm,

        allow_delegation=False,

        verbose=False,

        max_iter=8,
    )

    research_task = Task(
        description=f"""
Research the following topic:

{topic}

Use the DuckDuckGo Web Search tool to gather relevant information from the
internet before writing the report.

Research requirements:

- Search for multiple relevant sources.
- Prefer authoritative sources such as official organizations, universities,
  research institutions, reputable publications, and primary sources.
- Use recent information when the topic depends on current facts.
- Compare important claims across sources where appropriate.
- Do not invent facts, statistics, URLs, quotations, or citations.
- Clearly distinguish web-researched information from your own synthesis.
- If a requested fact cannot be verified, say so instead of guessing.

Write the final report in Markdown with exactly these main sections:

# [Clear Research Title]

## Introduction

Briefly introduce the topic and explain why it matters.

## Key Findings

Give the most important findings in concise bullet points.

## Detailed Analysis

Explain the topic in useful detail. Organize with subheadings when helpful.

## Important Facts/Data

Include verified statistics, dates, measurements, comparisons, or other
important factual information when available.

If reliable numerical data is not available, state that clearly.

## Conclusion

Summarize the main conclusions without introducing unsupported claims.

## Sources / References

List the web sources actually used.

Include source title and URL.

Do not create references that were not returned by the web search.

Keep the report professional, readable, factual, and suitable for a student
research assignment or presentation.
""",

        expected_output=(
            "A complete Markdown research report with the required sections "
            "and a Sources / References section containing the URLs of sources "
            "actually used during web research."
        ),

        agent=researcher,
    )

    return Crew(
        agents=[researcher],
        tasks=[research_task],
        process="sequential",
        verbose=False,
    )


# ----------------------------
# Run research
# ----------------------------

def run_research(topic: str):
    """Run the CrewAI research crew and return the final report."""

    api_key = get_groq_api_key()

    if not api_key:

        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your local .env file "
            "or Streamlit Cloud Secrets."
        )

    crew = create_research_crew(
        api_key,
        topic,
    )

    result = crew.kickoff()

    # CrewAI's final result is normally available as .raw
    report = getattr(
        result,
        "raw",
        str(result),
    )

    return report


# ----------------------------
# Streamlit user interface
# ----------------------------

st.markdown(
    """
<div class="hero">
    <h1>Research any topic,<br><span class="glow">with sources.</span></h1>
    <p>
        Enter a topic. A CrewAI agent searches the web, reads what it finds,
        and writes a structured report you can download.
    </p>
</div>
<div class="pills">
    <span class="pill"><b>Agent</b> CrewAI</span>
    <span class="pill"><b>Search</b> DuckDuckGo</span>
    <span class="pill"><b>Model</b> Groq GPT-OSS 120B</span>
</div>
""",
    unsafe_allow_html=True,
)

st.divider()


topic = st.text_area(
    "Research Topic",
    placeholder="Example: Impact of Artificial Intelligence on Education",
    height=120,
)


col1, col2 = st.columns(
    [1, 3]
)


with col1:

    research_button = st.button(
        "🔍 Research",
        type="primary",
        use_container_width=True,
    )


# ----------------------------
# Research button
# ----------------------------

if research_button:

    if not topic.strip():

        st.warning(
            "Please enter a research topic first."
        )

    elif len(topic.strip()) < 5:

        st.warning(
            "Please enter a more specific research topic."
        )

    else:

        with st.spinner(
            "Researching the topic and preparing your report..."
        ):

            try:

                report = run_research(
                    topic.strip()
                )

                st.session_state["research_topic"] = (
                    topic.strip()
                )

                st.session_state["research_report"] = report

            except Exception as error:

                st.error(
                    "The research process could not be completed."
                )

                st.exception(error)


# ----------------------------
# Display research report
# ----------------------------

if "research_report" in st.session_state:

    st.divider()

    with st.container(border=True):

        st.markdown(
            '<div class="report-head">📄 Research Report</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="report-meta">Topic: '
            f'{st.session_state.get("research_topic", "")}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            st.session_state["research_report"]
        )

    st.download_button(
        label="⬇️ Download Report",

        data=st.session_state["research_report"],

        file_name="research_report.md",

        mime="text/markdown",
    )


# ----------------------------
# Footer
# ----------------------------

st.divider()

st.caption(
    "Built with CrewAI • Groq • DuckDuckGo • Streamlit"
)