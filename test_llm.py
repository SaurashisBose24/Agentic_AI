from core import ollama_client

llm = ollama_client.OllamaClient()

#llm = OllamaClient()

prompt = """
Return:
{
  "message": "hello world"
}
"""

response = llm.generate_json(prompt)

print(response)