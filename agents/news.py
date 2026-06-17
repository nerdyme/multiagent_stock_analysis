import json
import os

import yfinance as yf
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class NewsAgent:

    def __init__(self, model="gpt-4.1-mini"):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model

    def get_headlines(self, ticker, limit=10):

        stock = yf.Ticker(ticker)

        try:
            news = stock.news[:limit]
        except Exception:
            return []

        headlines = []

        for item in news:

            title = item.get("title")

            if title:
                headlines.append(title)

        return headlines

    def analyze_with_llm(self, headlines):

        if not headlines:
            return {
                "agent": "news",
                "vote": "HOLD",
                "confidence": 50,
                "reason": ["No recent news found"]
            }

        headlines_text = "\n".join(
            f"- {h}" for h in headlines
        )

        prompt = f"""
You are a stock market news analyst.

Analyze the following headlines.

Rules:

1. Determine whether sentiment is BUY, SELL, or HOLD.
2. Return confidence from 0-100.
3. Give up to 3 concise reasons.
4. Return JSON only.

Headlines:

{headlines_text}

Expected JSON:

{{
  "vote":"BUY",
  "confidence":80,
  "reason":[
    "Reason 1",
    "Reason 2",
    "Reason 3"
  ]
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        try:

            result = json.loads(content)

            return {
                "agent": "news",
                "vote": result["vote"],
                "confidence": result["confidence"],
                "reason": result["reason"]
            }

        except Exception:

            return {
                "agent": "news",
                "vote": "HOLD",
                "confidence": 50,
                "reason": [
                    "Could not parse LLM response"
                ]
            }

    def run(self, ticker):

        headlines = self.get_headlines(ticker)

        return self.analyze_with_llm(
            headlines
        )