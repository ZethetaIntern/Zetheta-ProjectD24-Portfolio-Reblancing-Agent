# Tax-lot-aware educational optimisation.

from datetime import date

def classify_lot(purchase_date, today=None):
    today = today or date.today()
    held_days = (today - purchase_date).days
    return "LTCG" if held_days >= 365 else "STCG"

class TaxOptimiser:
    def optimise(self, portfolio, trades):
        # The simplified simulator estimates taxes on sale proceeds.
        sells = [t for t in trades if t["action"] == "SELL"]
        sell_value = sum(t["trade_value"] for t in sells)
        rate = float(portfolio["tax_rate"])
        estimated_tax = sell_value * rate * .25
        return {
            "sell_value": sell_value,
            "estimated_tax": estimated_tax,
            "tax_rate": rate,
            "tax_loss_harvesting": estimated_tax > 0,
            "wash_sale_check": "REQUIRED_BEFORE_REAL_EXECUTION",
        }
