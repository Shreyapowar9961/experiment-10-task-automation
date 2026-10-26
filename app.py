
import logging
import os
import time

import streamlit as st
from ddgs import DDGS
from langchain_groq import ChatGroq

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Configure Streamlit
st.set_page_config(
    page_title="Task Automation Agent",
    page_icon="🔎",
    layout="centered",
)

st.title("Task Automation Agent")
st.write(
    "Search the web and generate a concise three-point research brief."
)


def search_web(topic):
    """Search the web and handle temporary search failures."""
    try:
        results = list(DDGS().text(topic, max_results=5))
        formatted_results = []

        for result in results:
            formatted_results.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('href', '')}\n"
                f"Snippet: {result.get('body', '')}"
            )

        logger.info(
            "Search completed. Results found: %d",
            len(formatted_results),
        )
        return "\n\n".join(formatted_results)

    except Exception as exc:
        logger.warning("Web search failed: %s", exc)
        raise RuntimeError(
            "Web search is temporarily unavailable. "
            "Check your internet connection and try again."
        ) from exc


def summarize_results(topic, raw_results):
    """Summarize search results using the Groq API."""
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is not configured.")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=api_key,
        temperature=0,
    )

    prompt = f"""
You are a research assistant.

Research topic: {topic}

Web search results:
{raw_results}

Instructions:
- Use only information supported by the search results.
- Return exactly three concise bullet points.
- Do not include an introduction or conclusion.
- Do not invent facts or unsupported claims.
- If the evidence is insufficient, clearly state this.

Return only the three bullet points.
"""

    response = llm.invoke(prompt)
    content = response.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts = []

        for item in content:
            if isinstance(item, str):
                text_parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            elif hasattr(item, "text"):
                text_parts.append(item.text)

        return "\n".join(text_parts).strip()

    return str(content).strip()


# User interface
topic = st.text_input(
    "Enter a research topic",
    placeholder="e.g., Recent developments in renewable energy",
)

if st.button("Generate Research Brief", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")

    elif not os.environ.get("GROQ_API_KEY"):
        st.error(
            "Groq API key is not configured. "
            "Set GROQ_API_KEY in your environment and restart the app."
        )

    else:
        start_time = time.perf_counter()
        clean_topic = topic.strip()

        logger.info("Research topic received: %s", clean_topic)

        try:
            with st.spinner("Searching the web..."):
                raw_results = search_web(clean_topic)

            if not raw_results.strip():
                st.warning(
                    "No search results found. Please try another topic."
                )
            else:
                with st.spinner("Generating research brief with Groq..."):
                    brief = summarize_results(clean_topic, raw_results)

                if not brief:
                    st.warning(
                        "The summarizer returned an empty response. "
                        "Please try again."
                    )
                else:
                    st.subheader("Research Brief")
                    st.markdown(brief)

        except Exception as exc:
            logger.exception("Research request failed.")

            error_text = str(exc).lower()
            if "429" in error_text or "rate limit" in error_text:
                st.error(
                    "The Groq API rate limit has been reached. "
                    "Please check your Groq Console limits and try again later."
                )
            else:
                st.error(
                    "The request failed. Check the VS Code terminal "
                    "for the error details."
                )

        finally:
            elapsed = time.perf_counter() - start_time
            logger.info("Request completed in %.2f seconds.", elapsed)
