from graph import build_graph
from schemas import ResearchState

TEST_QUERIES = [
    "How does retrieval augmented generation work?",
    "What is LangGraph and how does it work?",
    "Explain vector databases and their use cases"
]

def test_pipeline():
    graph = build_graph()
    results = []

    for query in TEST_QUERIES:
        print(f"\nTesting: {query}")
        
        # single pass
        single = graph.invoke(ResearchState(query=query, max_iterations=1))
        
        # full pipeline
        full = graph.invoke(ResearchState(query=query, max_iterations=3))

        assert full["final_report"] is not None, "No report generated"
        assert full["iteration"] <= 3, "Exceeded max iterations"

        results.append({
            "query": query,
            "single_pass_score": single["coverage_score"],
            "final_score": full["coverage_score"],
            "iterations": full["iteration"],
            "report_length": len(full["final_report"])
        })

    # summary table
    print("\n--- Pipeline Evaluation Results ---")
    print(f"{'Query':<45} {'Single':>8} {'Final':>8} {'Iters':>7} {'Length':>8}")
    print("-" * 80)
    
    for r in results:
        print(
            f"{r['query'][:44]:<45}"
            f"{r['single_pass_score']:>8.2f}"
            f"{r['final_score']:>8.2f}"
            f"{r['iterations']:>7}"
            f"{r['report_length']:>8}"
        )

    # averages
    avg_single = sum(r["single_pass_score"] for r in results) / len(results)
    avg_final = sum(r["final_score"] for r in results) / len(results)
    improvement = ((avg_final - avg_single) / avg_single) * 100

    print("-" * 80)
    print(f"{'Average':<45}{avg_single:>8.2f}{avg_final:>8.2f}")
    print(f"\nLoop improvement: {improvement:.1f}% over single pass")

if __name__ == "__main__":
    test_pipeline()