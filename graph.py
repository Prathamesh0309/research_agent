from langgraph.graph import StateGraph, END
from schemas import ResearchState
from agents.planner import run_planner
from agents.searcher import run_searcher
from agents.critic import run_critic
from agents.writer import run_writer

# --- Decision function (the brain of the loop) ---
def should_continue(state: ResearchState):
    if state.iteration >= state.max_iterations:
        return "writer"        # force forward, no infinite loops
    if state.has_gaps and state.coverage_score < 0.75:
        return "searcher"      # loop back, search more
    return "writer"            # good enough, write the report

# --- Build the graph ---
def build_graph():
    graph = StateGraph(ResearchState)

    # Add all agents as nodes
    graph.add_node("planner", run_planner)
    graph.add_node("searcher", run_searcher)
    graph.add_node("critic", run_critic)
    graph.add_node("writer", run_writer)

    # Define the flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "critic")
    
    # This is the conditional edge — the ReAct loop
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "searcher": "searcher",
            "writer": "writer"
        }
    )
    
    graph.add_edge("writer", END)

    return graph.compile()