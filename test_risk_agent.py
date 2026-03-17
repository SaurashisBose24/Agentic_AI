from agents import risk_agent
#
agent = risk_agent.RiskAgent()

project_output = {
    "delay_risk": True,
    "budget_risk": True,
    "risk_level": "HIGH",
    "summary": "Project delayed and over budget"
}

market_output = {
    "market_risk": "HIGH",
    "risk_score": 0.8,
    "affected_areas": ["supply chain"],
    "summary": "Supply chain disruption"
}

result = agent.analyze(project_output, market_output)

print(result)