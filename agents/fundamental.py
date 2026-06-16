import yfinance as yf


class FundamentalAgent:

    def __init__(self):
        pass

    def run(self, ticker):

        stock = yf.Ticker(ticker)

        info = stock.info

        pe = info.get("trailingPE")
        revenue_growth = info.get("revenueGrowth")
        roe = info.get("returnOnEquity")

        score = 0
        reasons = []

        if revenue_growth and revenue_growth > 0:
            score += 1
            reasons.append("Positive revenue growth")

        if roe and roe > 0.15:
            score += 1
            reasons.append("Strong ROE")

        if pe and pe < 30:
            score += 1
            reasons.append("Reasonable valuation")

        if score >= 3:
            vote = "BUY"
        elif score == 2:
            vote = "HOLD"
        else:
            vote = "SELL"

        confidence = int((score / 3) * 100)

        return {
            "agent": "fundamental",
            "vote": vote,
            "confidence": confidence,
            "reason": reasons
        }