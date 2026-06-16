from agents.technical import TechnicalAgent
from agents.fundamental import FundamentalAgent
from agents.news import NewsAgent
from agents.decision import DecisionAgent


ticker = "INFY.NS"
print("main.py started")
technical = TechnicalAgent()
fundamental = FundamentalAgent()
news = NewsAgent()

results = []

results.append(
    technical.run(ticker)
)

results.append(
    fundamental.run(ticker)
)

results.append(
    news.run(ticker)
)

decision_agent = DecisionAgent()

final_result = decision_agent.run(
    results
)

print("\nAGENT OUTPUTS\n")

for r in results:
    print(r)

print("\nFINAL DECISION\n")

print(final_result)