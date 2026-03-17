from core import ollama_client

class ReportingAgent:
    def __init__(self):
        self.llm = ollama_client.OllamaClient()

    def generate_report(self, project_data, final_risk):
        prompt = f"""
You are a project risk reporting assistant.

Project Data:
{project_data}

Risk Analysis:
{final_risk}

Generate a clear, concise report.

Include:
- Risk Level
- Key Issues
- Recommendations

Keep it simple and professional.

Return plain text (NOT JSON).
"""

        response = self.llm.generate(prompt)
        return response