import yfinance as yf


class NewsAgent:

    POSITIVE_WORDS = [
        "growth",
        "record",
        "beat",
        "surge",
        "profit",
        "strong",
        "upgrade"
    ]

    NEGATIVE_WORDS = [
        "lawsuit",
        "decline",
        "miss",
        "downgrade",
        "loss",
        "weak",
        "investigation"
    ]

    def __init__(self):
        pass

    def run(self, ticker):

        stock = yf.Ticker(ticker)

        try:
            news = stock.news[:10]
        except Exception:
            news = []

        positive = 0
        negative = 0

        reasons = []

        for item in news:

            title = item.get("title", "").lower()

            for word in self.POSITIVE_WORDS:
                if word in title:
                    positive += 1

            for word in self.NEGATIVE_WORDS:
                if word in title:
                    negative += 1

        if positive > negative:
            vote = "BUY"
            confidence = 70
            reasons.append("News sentiment positive")

        elif negative > positive:
            vote = "SELL"
            confidence = 70
            reasons.append("News sentiment negative")

        else:
            vote = "HOLD"
            confidence = 50
            reasons.append("Mixed news sentiment")

        return {
            "agent": "news",
            "vote": vote,
            "confidence": confidence,
            "reason": reasons
        }