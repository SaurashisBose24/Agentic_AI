from core import ollama_client


class ProjectAgent:
    def __init__(self):
        self.llm = ollama_client.OllamaClient()

    def analyze(self, project_data):
        prompt = f"""
You are a project risk analysis expert.

Analyze the following project data:

Project Data:
{project_data}

Check:
- If completion_date > deadline → delay risk
- If budget_used > budget_allocated → budget risk

Return ONLY valid JSON:
{{
  "delay_risk": true/false,
  "budget_risk": true/false,
  "risk_level": "LOW/MEDIUM/HIGH",
  "summary": "short explanation"
}}
"""

        response = self.llm.generate_json(prompt)
        return response