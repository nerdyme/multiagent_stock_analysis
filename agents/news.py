import json
import os

import yfinance as yf
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


class NewsAgent:

    def __init__(self, model="claude-3-5-sonnet-20240620"):
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
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
            if not title and isinstance(item.get("content"), dict):
                title = item["content"].get("title")

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
            )
        except Exception as exc:
            return self._fallback_response(f"LLM request failed: {exc}")

        text_blocks = [
            block.text for block in response.content if block.type == "text"
        ]
        content = "".join(text_blocks)

        if not content.strip():
            return self._fallback_response("Empty LLM response")

        try:
            result = json.loads(content)
            return {
                "agent": "news",
                "vote": result["vote"],
                "confidence": result["confidence"],
                "reason": result["reason"],
            }
        except (json.JSONDecodeError, KeyError, TypeError):
            return self._fallback_response("Could not parse LLM response")

    def _fallback_response(self, reason):
        return {
            "agent": "news",
            "vote": "HOLD",
            "confidence": 50,
            "reason": [reason],
        }

    def run(self, ticker):

        headlines = self.get_headlines(ticker)

        return self.analyze_with_llm(
            headlines
        )