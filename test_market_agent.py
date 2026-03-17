#from agents.market_agent import MarketAgent
#
#agent = MarketAgent()
from agents import market_agent

agent = market_agent.MarketAgent()


market_data = [
    "Global supply chain disruption affecting electronics",
    "Inflation rising, material costs increasing"
]

result = agent.analyze(market_data)

print(result)