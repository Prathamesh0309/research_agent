import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,       # slight creativity for better writing
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def run_writer(state):
    '''Takes the search results and crafts a structured research report. 
    If the critic identified gaps, it emphasizes those in the report.'''
    
    results_text = ""
    for r in state.search_results:
        results_text += f"\nSource: {r['title']} ({r['url']})\nContent: {r['content'][:400]}\n"

    prompt = f"""
    Write a structured research report answering this query:
    {state.query}
    
    Use these sub-questions as your section headings:
    {chr(10).join(state.sub_questions)}
    
    Source material:
    {results_text}
    
    Format:
    - A 2 sentence executive summary at the top
    - One section per sub-question
    - Cite sources as [Source Title] inline
    - End with a "Key Takeaways" section (3 bullet points)
    
    Be concise. Prioritize clarity over length.
    """

    response = llm.invoke([
        SystemMessage(content="You are an expert research writer."),
        HumanMessage(content=prompt)
    ])

    return state.model_copy(update={"final_report": response.content})