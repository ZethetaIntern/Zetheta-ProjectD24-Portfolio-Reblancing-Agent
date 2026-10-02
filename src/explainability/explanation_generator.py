# Groq-powered explanation generator with deterministic fallback.

import os
from dotenv import load_dotenv
load_dotenv()

try:
    from langchain_groq import ChatGroq
except Exception:
    ChatGroq = None

class ExplanationGenerator:
    def __init__(self):
        self.key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.llm = None
        if self.key and ChatGroq:
            self.llm = ChatGroq(
                api_key=self.key,
                model=self.model,
                temperature=.2,
            )

    def _facts(self, audience, portfolio, drift, trigger, recommendation):
        trades = recommendation.get("trades", [])
        trade_text = "; ".join(
            f'{x["action"]} {x["asset"]} {x["weight_change"]:+.2%}'
            for x in trades
        ) or "No trades."

        return (
            f"Portfolio: {portfolio['portfolio_id']}\n"
            f"Risk category: {portfolio['risk_category']}\n"
            f"Trigger: {trigger['type']} / {trigger['priority']}\n"
            f"Reason: {trigger['reason']}\n"
            f"Maximum drift: {drift['max_drift']:.2%}\n"
            f"Drift band: {drift['band']:.2%}\n"
            f"Turnover: {recommendation['optimisation'].get('turnover', 0):.2%}\n"
            f"Trades: {trade_text}\n"
            f"Estimated tax: ₹{recommendation['tax']['estimated_tax']:,.2f}\n"
            f"Estimated cost: ₹{recommendation['cost']['total_cost']:,.2f}\n"
            f"Compliance passed: {recommendation['compliance']['passed']}\n"
            f"Audience: {audience}\n"
        )

    def _fallback(self, audience, portfolio, drift, trigger, recommendation):
        facts = self._facts(audience, portfolio, drift, trigger, recommendation)
        if audience == "client":
            return (
                "This simulated review found that the portfolio moved outside its "
                "configured allocation band. " + facts +
                "\nThis is an educational simulation and does not place a real trade."
            )
        if audience == "advisor":
            return "Advisor decision record:\n" + facts
        return "Compliance decision record:\n" + facts

    def generate(self, audience, portfolio, drift, trigger, recommendation):
        fallback = self._fallback(audience, portfolio, drift, trigger, recommendation)
        if not self.llm:
            return fallback

        prompt = f"""
You are an explanation-writing component for a portfolio rebalancing simulator.
Use ONLY the supplied facts. Never invent financial data, tax rates, regulations,
returns, guarantees or execution status.

{fallback}

Write a concise explanation for the specified audience.
Preserve numerical facts exactly.
"""
        try:
            return self.llm.invoke(prompt).content
        except Exception:
            # Groq outages or quota errors must not break the application.
            return fallback
