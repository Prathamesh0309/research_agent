import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
# results = client.search("what is agentic AI", max_results=3)

# for r in results["results"]:
#     print(r["title"])
#     print(r["url"])
#     print(r["content"][:200])  # first 200 chars
#     print("---")

from langchain_google_genai import ChatGoogleGenerativeAI


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
print("")
response = llm.invoke("say hello in one word")
print(response.content)