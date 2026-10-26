# Task Automation Agent

A Streamlit application that searches the web using DuckDuckGo and summarizes results using the Groq API.

## Technologies
- Python 3.11
- Streamlit
- LangChain
- Groq
- DuckDuckGo Search
- Docker
- GitHub Actions

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the GROQ_API_KEY environment variable, then run:

```bash
streamlit run app.py
```

## Run with Docker

Build:

```bash
docker build -t task-automation-agent .
```

Run:

```bash
docker run --rm -p 8501:8501 -e GROQ_API_KEY task-automation-agent
```

Open http://localhost:8501.

## Continuous Integration

GitHub Actions checks Python syntax, runs automated tests, and builds a Docker image on pushes and pull requests to main.

## Security

Never commit API keys, .env files, or other secrets.
