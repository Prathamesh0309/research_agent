# Personal Research Assistant Agent

A multi-agent AI pipeline that autonomously researches any topic — breaking down queries, searching the web iteratively, critiquing coverage, and synthesizing structured reports with citations.

Built as a portfolio project to demonstrate real-world agentic AI engineering techniques.

---

## What it does

Most search-and-summarize tools run one query and call it done. This system thinks like a researcher:

1. **Decomposes** your query into focused sub-questions
2. **Searches** the web for each sub-question via Tavily
3. **Critiques** the coverage — are there gaps? Is it deep enough?
4. **Loops back** to search again if gaps are found (ReAct pattern)
5. **Writes** a structured markdown report with inline citations

---

## Architecture

```
User Query
    ↓
[Planner Agent]       → breaks query into 4-6 sub-questions
    ↓
[Searcher Agent]      → Tavily search per sub-question, appends to state
    ↓
[Critic Agent]        → scores coverage (0–1), identifies gaps
    ↓         ↑ ReAct loop (max 3 iterations)
[Writer Agent]        → synthesizes final report with citations
    ↓
Markdown Report
```

All agents share a single typed `ResearchState` object (Pydantic) orchestrated via LangGraph.

---

## Tech Stack

| Component | Tool |
|---|---|
| Orchestration | LangGraph |
| LLM | Gemini 2.0 Flash (`langchain-google-genai`) |
| Web Search | Tavily API |
| Structured Output | Pydantic v2 |
| State Management | LangGraph `StateGraph` |
| Evaluation | Custom coverage scoring |

---

## Project Structure

```
research-agent/
├── main.py                  # entry point
├── graph.py                 # LangGraph state graph + routing logic
├── schemas.py               # shared ResearchState (Pydantic)
├── agents/
│   ├── planner.py           # query decomposition
│   ├── searcher.py          # Tavily search + result accumulation
│   ├── critic.py            # coverage scoring + gap detection
│   └── writer.py            # report synthesis
└── eval/
    ├── test_agents.py       # unit tests per agent
    └── test_pipeline.py     # end-to-end evaluation across queries
```

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/prathamesh0309/research-agent
cd research-agent
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install langgraph langchain-google-genai tavily-python pydantic python-dotenv
```

### 3. Configure API keys

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Get your keys:
- Gemini: https://aistudio.google.com
- Tavily: https://app.tavily.com

### 4. Run

```bash
python main.py
```

To change the query, edit the `run()` call in `main.py`:

```python
run("your research topic here")
```

---

## How it works — key concepts

### Shared State
Every agent receives and returns a `ResearchState` object. This is how agents communicate — not by calling each other directly, but by reading and writing to a shared typed state. No agent mutates state in place; each returns a new copy.

### ReAct Loop
After the Searcher runs, the Critic evaluates coverage on three dimensions: breadth (all sub-questions addressed?), depth (enough detail?), and recency (current information?). If the score falls below the threshold and the iteration limit hasn't been reached, the graph routes back to the Searcher.

```python
def should_continue(state):
    if state.iteration >= state.max_iterations:
        return "writer"
    if state.has_gaps and state.coverage_score < 0.65:
        return "searcher"
    return "writer"
```

### Gap-aware Re-search
On re-search iterations, the Searcher doesn't repeat the same sub-questions. Instead it searches using the Critic's `gap_summary` — a concise description of what's missing. This makes each loop meaningfully different from the last.

---

## Design Decisions

### Problem: Critic became a harsh grader over multiple iterations
As the ReAct loop accumulated results across iterations, the Critic was receiving a growing, noisy context window. This caused coverage scores to drop inconsistently — from 0.70 on iteration 1 down to 0.47 on iteration 3 — even when the actual content quality had improved.

### Solution: Result windowing + content truncation
Three targeted fixes stabilised Critic scoring:

- **Result windowing** — pass only the last 12 results to the Critic, not the full accumulated set
- **Content truncation** — cap each result's content at 150 characters to reduce noise
- **Constrained gap summaries** — prompt the Critic to describe gaps in 10 words or less, making them precise enough to double as Tavily search queries

These are deliberate tradeoffs: some context is lost, but evaluation stability and search precision improve significantly.

---
<!-- 
## Evaluation

Tested across 3 queries comparing single-pass (no loop) vs full iterative pipeline:

| Query | Single Pass | Final Score | Iterations |
|---|---|---|---|
| How does RAG work? | 0.65 | — | 3 |
| What is LangGraph? | 0.60 | — | 3 |
| Explain vector databases | 0.60 | — | 3 |
| **Average** | **0.62** | **—** | **3** |
-->

To run evaluation:
```bash
python eval/test_pipeline.py
```

---

## Interview talking points

- **Multi-agent orchestration** — 4 specialized agents with typed state, each testable in isolation
- **ReAct pattern** — Critic reasons about gaps, Searcher acts on that reasoning, loop repeats until confident
- **Gap-aware re-search** — re-search uses the Critic's gap summary, not the original sub-questions
- **Result windowing** — diagnosed and fixed Critic context-overload through deliberate tradeoffs
- **Structured outputs throughout** — every agent uses Pydantic, no raw string parsing anywhere

---

## What I'd add next

- **ChromaDB memory layer** — deduplicate sources across runs so the same URL is never fetched twice
- **Streamlit UI** — live progress view showing which agent is running and current coverage score
- **RAGAS evaluation** — formal RAG evaluation metrics alongside the custom coverage scorer
- **Async search** — run sub-question searches in parallel instead of sequentially

---

## License

MIT
