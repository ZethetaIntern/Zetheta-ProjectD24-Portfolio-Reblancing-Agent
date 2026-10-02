# Human override capture.

from datetime import datetime

class OverrideCapture:
    def capture(self, portfolio_id, action, reason):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "portfolio_id": portfolio_id,
            "action": action,
            "reason": reason,
        }
