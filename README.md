# Research Agent Prototype

A lightweight research agent prototype that breaks a query into focused research questions, gathers web evidence, evaluates coverage, and generates a final report.

## What’s included

- `schemas.py` — shared `ResearchState` model for the research loop
- `graph.py` — constructs the LangGraph state machine and orchestrates the agent flow
- `main.py` — entry point for running the full pipeline on a sample query
- `test_pipeline.py` — simple pipeline evaluation harness with sample queries
- `agents/planner.py` — generates focused sub-questions using Gemini
- `agents/searcher.py` — gathers web evidence via Tavily
- `agents/critic.py` — scores coverage and identifies gaps
- `agents/writer.py` — writes a structured research report from the gathered evidence

## Current status

This project is an early-stage prototype.

- A graph-based pipeline now runs planner → searcher → critic → writer
- The critic can loop back to the searcher when coverage is insufficient
- A final report writer is implemented
- Production-ready packaging, robust error handling, and broader test coverage are still pending

## Requirements

- Python 3.13
- A virtual environment is strongly recommended
- `research-agent/` is currently used as the local virtual environment directory

## Environment variables

Create a `.env` file at the repository root with these keys:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Install dependencies

From the repository root:

```bash
source research-agent/bin/activate
pip install python-dotenv pydantic langchain-google-genai tavily
```

## Run the prototype

Run the main pipeline:

```bash
source research-agent/bin/activate
python main.py
```

Run the pipeline evaluator:

```bash
source research-agent/bin/activate
python test_pipeline.py
```

## How it works

1. `main.py` builds the graph from `graph.py` and initializes a `ResearchState`
2. `planner.py` generates sub-questions from the user query
3. `searcher.py` gathers evidence for the sub-questions (or for gap summaries)
4. `critic.py` scores coverage and decides whether to loop back or proceed
5. `writer.py` generates a final structured research report

## Notes

- The project depends on Google Gemini via `langchain_google_genai`
- The `tavily` client is used for external search results
- Keep API keys private and do not commit them to source control

## Future work

- improve error handling and retries for API failures
- add more robust test coverage for each agent step
- support configurable loop policies and dynamic stopping criteria
- add a final answer synthesis and report summary export
