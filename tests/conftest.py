import os
import sys

# The agent modules build their LLM clients at import time. Dummy keys let the
# tests import them without any network access; no test makes a real API call.
os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("TAVILY_API_KEY", "test-key")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
