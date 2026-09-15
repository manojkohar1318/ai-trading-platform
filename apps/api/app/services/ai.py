from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system: str, user: str, context: dict) -> str:
        ...


class MockLLMProvider(LLMProvider):
    def generate(self, system: str, user: str, context: dict) -> str:
        analysis = context.get("analysis")
        if not analysis:
            return (
                "DEMO AI: I can perform quantitative market analysis. "
                "Ask about a specific NSE stock such as RELIANCE, TCS or INFY."
            )

        quote = analysis.get("quote", {})
        score = analysis.get("score", {})
        setup = analysis.get("trade_setup")
        trend = analysis.get("trend", "neutral")

        price = quote.get("price", 0)
        total = score.get("total_score", 0)

        lines = [
            f"Analysis for {quote.get('symbol', 'the selected stock')}:",
            f"Price: ₹{price:.2f}",
            f"Trend: {trend.upper()}",
            f"Quant score: {total}/100",
        ]

        if setup:
            lines.append(
                f"Trade setup: {setup.get('direction', 'N/A').upper()} | "
                f"Entry zone: {setup.get('entry_zone')} | "
                f"Target: {setup.get('target')} | "
                f"Stop-loss: {setup.get('stop_loss')}"
            )
        else:
            lines.append("Trade setup: NO TRADE SETUP")

        lines.append(
            "This is quantitative analysis using available market data, "
            "not a guarantee of future returns."
        )
        return "\n".join(lines)


class TradingAIService:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def answer(self, question: str, analysis: dict | None = None) -> str:
        system = (
            "You are an Indian stock-market quantitative analysis assistant. "
            "Never guarantee profits or outcomes. Clearly distinguish demo "
            "data from live market data."
        )
        return self.llm.generate(
            system,
            question,
            {"analysis": analysis} if analysis else {},
        )
