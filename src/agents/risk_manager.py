# Risk Manager agent.

from src.optimisation.liquidity_scorer import score

class RiskManager:
    def run(self, portfolio, recommendation):
        recommendation["liquidity"] = score(
            portfolio, recommendation["trades"]
        )
        recommendation["risk"] = {
            "turnover": recommendation["optimisation"].get("turnover", 1),
            "equity_after": recommendation["optimisation"].get("post_trade", {}).get(
                "indian_equity", 0
            ) + recommendation["optimisation"].get("post_trade", {}).get(
                "international_equity", 0
            ),
        }
        return recommendation
