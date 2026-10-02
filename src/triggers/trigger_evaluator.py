# Combine threshold, calendar and event triggers.

from datetime import datetime

class TriggerEvaluator:
    def evaluate(self, portfolio, drift, event="None"):
        triggers = []

        if drift["max_drift"] > drift["band"]:
            triggers.append(("THRESHOLD", "HIGH",
                             f"Maximum drift {drift['max_drift']:.2%} exceeds {drift['band']:.2%}."))

        if int(portfolio["days_since_rebalance"]) >= 90:
            triggers.append(("CALENDAR", "MEDIUM", "Quarterly review interval reached."))

        if event != "None":
            triggers.append(("EVENT", "CRITICAL", f"Event trigger: {event}."))

        if not triggers:
            return {"triggered": False, "type": "NONE", "priority": "LOW",
                    "reason": "No trigger fired.", "timestamp": datetime.utcnow().isoformat()}

        priority_order = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1}
        selected = max(triggers, key=lambda x: priority_order[x[1]])
        return {
            "triggered": True,
            "type": selected[0],
            "priority": selected[1],
            "reason": selected[2],
            "all_triggers": [
                {"type": t[0], "priority": t[1], "reason": t[2]} for t in triggers
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }
