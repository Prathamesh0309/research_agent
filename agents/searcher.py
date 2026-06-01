import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def run_searcher(state):
    all_results = []

    for question in state.sub_questions:
        response = client.search(question, max_results=3)
        
        for r in response["results"]:
            all_results.append({
                "question": question,   # which sub-question this answers
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })

    return state.model_copy(update={
        "search_results": all_results,
        "iteration": state.iteration + 1
    })