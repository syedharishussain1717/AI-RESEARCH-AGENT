import os

import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Crew, LLM, Task
from crewai.tools import tool
from ddgs import DDGS


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

st.title("🔎 AI Research Agent")

st.markdown(
    "Enter a topic and let a **CrewAI research agent** search the web with "
    "**DuckDuckGo**, analyze the findings with **Groq GPT-OSS 120B**, "
    "and generate a structured research report."
)

st.divider()


topic = st.text_area(
    "Research Topic",
    placeholder="Example: Impact of Artificial Intelligence on Education",
    height=120,
)


col1, col2 = st.columns(
    [1, 5]
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

    st.subheader(
        "📄 Research Report"
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

