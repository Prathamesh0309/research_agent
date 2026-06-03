from schemas import ResearchState
from agents.planner import run_planner
from agents.searcher import run_searcher
from agents.critic import run_critic
from agents.writer import run_writer

state = ResearchState(query="How does retrieval augmented generation work?")
state = run_planner(state)
state = run_searcher(state)
state = run_critic(state)
state = run_writer(state)

print(state.final_report)