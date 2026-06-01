from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional


load_dotenv()

class ResearchState(BaseModel):
    query: str
    sub_questions: List[str] = []
    search_results: List[dict] = []     # what the searcher finds
    coverage_score: float = 0.0         # critic's verdict (0 to 1)
    has_gaps: bool = False              # critic's verdict (True = loop back)
    gap_summary: str = ""               # critic's feedback on what's missing
    iteration: int = 0                  # how many times we've looped
    max_iterations: int = 3
    final_report: Optional[str] = None