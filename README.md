# Research Agent Prototype

A lightweight research agent prototype for breaking a query into sub-questions, searching for answers, and evaluating coverage.

## What’s included

- `agents/schemas.py` — shared `ResearchState` model for the research loop
- `agents/planner.py` — generates focused sub-questions using Gemini
- `agents/searcher.py` — queries a search API for supporting content
- `agents/critic.py` — evaluates coverage and gap analysis
- `agents/test_planner.py` — example run of the planner and searcher pipeline

## Current status

This project is an early-stage prototype.

- The pipeline currently includes planning, search, and critique components
- A final synthesis/answer generation loop is not yet implemented
- Error handling, orchestration, and production-ready packaging are still pending

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
pip install -r requirements.txt
```

If `requirements.txt` is not present yet, install the main dependencies used in this prototype:

```bash
pip install python-dotenv pydantic langchain-google-genai tavily
```

## Run the prototype

```bash
source research-agent/bin/activate
python agents/test_planner.py
```

This will:

1. create a `ResearchState` for a sample query
2. generate sub-questions
3. run the searcher to collect results
4. print a small output summary

## Next steps

Potential next work includes:

- adding a loop that repeats search and critique until coverage is sufficient
- generating a final report or answer summary
- adding unit tests and validation for all components
- improving prompt design and output handling

## Notes

- The project currently depends on Google Gemini via `langchain_google_genai`
- The `tavily` search client is used for external search results
- Keep API keys private and do not commit them to source control
