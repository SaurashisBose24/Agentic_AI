#from core.ollama_client import OllamaClient
#from agents import market_agent
from core import ollama_client

#llm = ollama_client.OllamaClient()

class MarketAgent:
    def __init__(self):
        self.llm = ollama_client.OllamaClient()

    def analyze(self, market_data):
        prompt = f"""
You are a market risk analyst.

Analyze the following market news/events:

{market_data}

Tasks:
- Identify external risks affecting projects
- Classify overall market risk: LOW, MEDIUM, HIGH
- Assign a risk_score between 0 and 1
- Identify affected areas (e.g., supply chain, cost, resources)

Return ONLY valid JSON:
{{
  "market_risk": "LOW/MEDIUM/HIGH",
  "risk_score": number,
  "affected_areas": [],
  "summary": "short explanation"
}}
"""

        response = self.llm.generate_json(prompt)
        return response