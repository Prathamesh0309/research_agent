from schemas import ResearchState
from planner import run_planner
from searcher import run_searcher
from critic import run_critic
from writer import run_writer

state = ResearchState(query="How does retrieval augmented generation work?")
state = run_planner(state)
state = run_searcher(state)
state = run_critic(state)
state = run_writer(state)

print(state.final_report)