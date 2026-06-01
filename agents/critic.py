import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel

load_dotenv()

# --- Structured output schema ---
class CriticOutput(BaseModel):
    coverage_score: float      # 0.0 to 1.0
    has_gaps: bool             # True = loop back, False = move forward
    gap_summary: str           # what's missing (used if looping back)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def run_critic(state):
    # Format results so LLM can read them
    results_text = ""
    for r in state.search_results:
        results_text += f"\nQuestion: {r['question']}\nContent: {r['content'][:300]}\n"

    prompt = f"""
    Original query: {state.query}
    
    Sub-questions that need answering:
    {chr(10).join(state.sub_questions)}
    
    Content found so far:
    {results_text}
    
    Score the coverage from 0 to 1 on these 3 dimensions:
    1. Breadth — are all sub-questions addressed?
    2. Depth — is there enough detail per question?
    3. Recency — is the information current?
    
    Return an average score. If below 0.75, mark has_gaps as True
    and briefly describe what is missing in gap_summary.
    """

    structured_llm = llm.with_structured_output(CriticOutput)
    result = structured_llm.invoke([
        SystemMessage(content="You are a critical research evaluator."),
        HumanMessage(content=prompt)
    ])

    return state.model_copy(update={
        "coverage_score": result.coverage_score,
        "has_gaps": result.has_gaps,
        "gap_summary": result.gap_summary
    })