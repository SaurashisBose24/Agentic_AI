#from agents.project_agent import ProjectAgent
from agents import project_agent
#
agent = project_agent.ProjectAgent()

#agent = ProjectAgent()

sample_project = {
    "project_id": 1,
    "deadline": "2026-03-10",
    "completion_date": "2026-03-12",
    "budget_allocated": 10000,
    "budget_used": 12000
}

result = agent.analyze(sample_project)

print(result)