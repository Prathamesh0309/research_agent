import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# Tavily is our search engine. It provides an API to query the web and get structured results.
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def run_searcher(state):
    '''Searches the web for each sub-question and gathers results. If the critic identifies 
    gaps, it focuses the search on those gaps in subsequent iterations.'''

    all_results = []

    # If this is a subsequent iteration and the critic has identified a specific gap, search for that.
    if state.iteration > 0 and state.gap_summary:
        questions = [state.gap_summary]   # search for what's missing
    else:
        questions = state.sub_questions   # first run, use sub-questions

    # Search for each question and collect results
    for question in questions:
        response = client.search(question, max_results=3)
        
        # Each result includes a title, URL, and content snippet. We also tag it with which question it answers.
        for r in response["results"]:
            all_results.append({
                "question": question,   # which sub-question this answers
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })

    # Update the state with all the search results and increment the iteration count
    return state.model_copy(update={
        "search_results": all_results,
        "iteration": state.iteration + 1
    })