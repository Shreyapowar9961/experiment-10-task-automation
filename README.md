# Task Automation Agent

A Streamlit app that searches the web using DuckDuckGo and summarizes results using Groq.

## Run locally

Install dependencies:
pip install -r requirements.txt

Set the GROQ_API_KEY environment variable, then run:
streamlit run app.py

## Run with Docker

Build:
docker build -t task-automation-agent .

Run:
docker run --rm -p 8501:8501 -e GROQ_API_KEY task-automation-agent

Open http://localhost:8501.

Never commit API keys or secrets.
