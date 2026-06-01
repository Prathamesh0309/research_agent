import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List

load_dotenv()

# --- Structured output schema ---
class PlannerOutput(BaseModel):
    sub_questions: List[str]


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# --- Planner function ---
def run_planner(state):
    prompt = f"""
    You are a research planner. Break this query into 4 focused sub-questions
    that together would fully answer it. Each should target a distinct angle.
    
    Query: {state.query}
    """
    
    structured_llm = llm.with_structured_output(PlannerOutput)
    result = structured_llm.invoke([
        SystemMessage(content="You are a research planning assistant."),
        HumanMessage(content=prompt)
    ])
    
    return state.model_copy(update={"sub_questions": result.sub_questions})