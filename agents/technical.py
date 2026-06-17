import yfinance as yf
import pandas as pd
import ta


class TechnicalAgent:

    def __init__(self):
        pass

    def run(self, ticker):

        df = yf.download(
            ticker,
            period="1y",
            progress=False
        )

        if len(df) < 200:
            return {
                "agent": "technical",
                "vote": "HOLD",
                "confidence": 50,
                "reason": ["Insufficient data"]
            }

        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.squeeze(axis=1)

# simple moving average is a technical indicator that measures 
# the average price of a security over a period of time.
        sma50 = close.rolling(50).mean().iloc[-1]
        sma200 = close.rolling(200).mean().iloc[-1]

# Relative Strength Index
# it is a technical indicator that measures the speed and change of price movements.
# it is calculated using the following formula:
# RSI = 100 - 100 / (1 + RS)
# where RS is the average of the up days and the down days.
# the formula is:
# RS = average of the up days / average of the down days
# the formula is:
        rsi = ta.momentum.RSIIndicator(
            close
        ).rsi().iloc[-1]

        current_price = close.iloc[-1]

        reasons = []

        score = 0

        if current_price > sma50:
            score += 1
            reasons.append("Price above SMA50")

        if sma50 > sma200:
            score += 1
            reasons.append("Golden trend structure")

        if 40 <= rsi <= 70:
            score += 1
            reasons.append("Healthy RSI")

        if score >= 3:
            vote = "BUY"
        elif score == 2:
            vote = "HOLD"
        else:
            vote = "SELL"

        confidence = int((score / 3) * 100)

        return {
            "agent": "technical",
            "vote": vote,
            "confidence": confidence,
            "reason": reasons
        }