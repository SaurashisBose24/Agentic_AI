import requests
import json

class OllamaClient:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def generate(self, prompt, temperature=0.2):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        response = requests.post(self.url, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama Error: {response.text}")

        result = response.json()["response"]

        return result

    def generate_json(self, prompt):
        strict_prompt = f"""
You MUST return ONLY valid JSON.
No explanation. No extra text.
Ensure JSON is complete and properly closed.

    {prompt}
"""

        raw_output = self.generate(strict_prompt)

        #print("\n🔍 RAW LLM OUTPUT:\n", raw_output)

        cleaned = raw_output.strip()

        # Remove markdown
        cleaned = cleaned.replace("```json", "").replace("```", "")

        # 🔥 FIX: auto-close JSON if missing
        if not cleaned.endswith("}"):
            cleaned += "}"

        try:
            return json.loads(cleaned)
        except Exception as e:
            print("⚠️ JSON parsing failed. Attempting fallback...")

            # Try extracting JSON substring
            try:
                start = cleaned.find("{")
                end = cleaned.rfind("}") + 1
                return json.loads(cleaned[start:end])
            except:
                raise Exception(f"Invalid JSON from LLM:\n{raw_output}")