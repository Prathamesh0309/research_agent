from graph import build_graph
from schemas import ResearchState

def run(query: str):
    graph = build_graph()
    
    initial_state = ResearchState(query=query)
    final_state = graph.invoke(initial_state)
    
    print(f"\nIterations ran: {final_state['iteration']}")
    print(f"Final coverage score: {final_state['coverage_score']}")
    print("\n--- REPORT ---\n")
    print(final_state["final_report"])

if __name__ == "__main__":
    run("How does retrieval augmented generation work?")