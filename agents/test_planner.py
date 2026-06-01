from schemas import ResearchState
from planner import run_planner
from searcher import run_searcher

state = ResearchState(query="How does retrieval augmented generation work?")
state = run_planner(state)
state = run_searcher(state)

print(f"Total results: {len(state.search_results)}")
print(f"Iteration: {state.iteration}")
print("---")
print(state.search_results[0])  # peek at first results