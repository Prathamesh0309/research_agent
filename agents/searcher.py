import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

_client = None


def get_client():
    """Create the Tavily client on first use, so importing this module doesn't need an API key."""
    global _client
    if _client is None:
        _client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    return _client

def run_searcher(state):
    '''Searches the web for each sub-question and gathers results. If the critic identifies 
    gaps, it focuses the search on those gaps in subsequent iterations.'''

    new_results = []

    # If this is a subsequent iteration and the critic has identified a specific gap, search for that.
    if state.iteration > 0 and state.gap_summary:
        questions = [state.gap_summary]   # search for what's missing
    else:
        questions = state.sub_questions   # first run, use sub-questions

    # Search for each question and collect results
    for question in questions:
        response = get_client().search(question, max_results=3)
        
        # Each result includes a title, URL, and content snippet. We also tag it with which question it answers.
        for r in response["results"]:
            new_results.append({
                "question": question,   # which sub-question this answers
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })

    # Append to what earlier iterations found (rather than replacing it), and skip
    # URLs we already have, so each revision loop adds new material.
    seen_urls = {r["url"] for r in state.search_results}
    fresh = []
    for r in new_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            fresh.append(r)

    return state.model_copy(update={
        "search_results": state.search_results + fresh,
        "iteration": state.iteration + 1
    })
