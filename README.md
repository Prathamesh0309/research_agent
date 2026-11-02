# Personal Research Assistant Agent

A multi-agent pipeline that researches a topic on its own: it breaks the question into sub-questions, searches the web, critiques its own coverage, searches again if there are gaps, and writes a structured report with citations.

## What it does

Most search-and-summarize tools run one query and stop. This system works more like a researcher:

1. **Decomposes** your query into focused sub-questions
2. **Searches** the web for each sub-question via Tavily
3. **Critiques** the coverage: are there gaps, is it deep enough?
4. **Loops back** to search again if gaps are found (ReAct pattern)
5. **Writes** a structured markdown report with inline citations

<!-- Add a short example here: the query you ran and a snippet of the generated report. -->

## Architecture

```
User Query
    ↓
[Planner Agent]       → breaks query into 4–6 sub-questions
    ↓
[Searcher Agent]      → Tavily search per sub-question, appends to state
    ↓
[Critic Agent]        → scores coverage (0–1), identifies gaps
    ↓         ↑ ReAct loop (max 3 iterations)
[Writer Agent]        → synthesizes final report with citations
    ↓
Markdown Report
```

All agents share a single typed `ResearchState` object (Pydantic), orchestrated with a LangGraph `StateGraph`.

## Tech stack

| Component | Tool |
| --- | --- |
| Orchestration | LangGraph |
| LLM | Gemini 2.0 Flash (`langchain-google-genai`) |
| Web search | Tavily API |
| Structured output | Pydantic v2 |
| Evaluation | Custom coverage scoring |

## Project structure

```
research_agent/
├── main.py                  # entry point
├── graph.py                 # LangGraph state graph + routing logic
├── schemas.py               # shared ResearchState (Pydantic)
├── agents/
│   ├── planner.py           # query decomposition
│   ├── searcher.py          # Tavily search + result accumulation
│   ├── critic.py            # coverage scoring + gap detection
│   └── writer.py            # report synthesis
└── evals/
    ├── test_agents.py       # unit tests per agent
    └── test_pipeline.py     # end-to-end evaluation across queries
```

## Setup

```bash
git clone https://github.com/Prathamesh0309/research_agent
cd research_agent
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install langgraph langchain-google-genai tavily-python pydantic python-dotenv
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Get keys: [Gemini](https://aistudio.google.com) · [Tavily](https://app.tavily.com)

Run:

```bash
python main.py
```

To change the query, edit the `run()` call in `main.py`:

```python
run("your research topic here")
```

Run the evaluation:

```bash
python evals/test_pipeline.py
```

## How it works

### Shared state
Agents don't call each other. Each one reads from and writes to a typed `ResearchState`. No agent mutates state in place; each returns a new copy.

### ReAct loop
After the Searcher runs, the Critic evaluates coverage on breadth (all sub-questions addressed?), depth (enough detail?) and recency (current information?). If the score is below the threshold and the iteration limit hasn't been reached, the graph routes back to the Searcher.

```python
def should_continue(state):
    if state.iteration >= state.max_iterations:
        return "writer"
    if state.has_gaps and state.coverage_score < 0.65:
        return "searcher"
    return "writer"
```

### Gap-aware re-search
On re-search iterations the Searcher doesn't repeat the original sub-questions. It searches using the Critic's `gap_summary`, a short description of what's missing, so each loop adds something new.

## Design decisions

**Problem: the Critic became a harsh grader over multiple iterations.**
As results accumulated, the Critic received a growing, noisy context. Coverage scores dropped from 0.70 on iteration 1 to 0.47 on iteration 3, even though content quality was improving.

**Solution: result windowing and content truncation.**
- **Result windowing:** pass only the last 12 results to the Critic
- **Content truncation:** cap each result's content at 150 characters
- **Constrained gap summaries:** limit gaps to 10 words so they double as precise search queries

These are deliberate tradeoffs: some context is lost, but scoring is stable and searches are more precise.

## What I'd add next

- **ChromaDB memory layer** to avoid fetching the same URL twice across runs
- **Streamlit UI** showing which agent is running and the current coverage score
- **RAGAS evaluation** alongside the custom coverage scorer
- **Async search** to run sub-question searches in parallel

## License

MIT
