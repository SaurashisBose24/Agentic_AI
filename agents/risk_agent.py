from core import ollama_client

class RiskAgent:
    def __init__(self):
        self.llm = ollama_client.OllamaClient()

    def analyze(self, project_risk, market_risk):
        prompt = f"""
You are a senior risk assessment expert.

Inputs:

Project Risk Analysis:
{project_risk}

Market Risk Analysis:
{market_risk}

Your job:
- Combine both analyses
- Assign a final risk score (0 to 1)
- Classify as LOW, MEDIUM, HIGH
- Identify key contributing factors

Rules:
- If both project + market risks are high → HIGH
- If one is high → MEDIUM/HIGH
- If both low → LOW

Return ONLY valid JSON:
{{
  "final_risk_score": number,
  "risk_level": "LOW/MEDIUM/HIGH",
  "key_factors": [],
  "justification": "short explanation"
}}
"""

        response = self.llm.generate_json(prompt)

        # Optional cleanup
        try:
            response["final_risk_score"] = float(response["final_risk_score"])
        except:
            pass

        return response