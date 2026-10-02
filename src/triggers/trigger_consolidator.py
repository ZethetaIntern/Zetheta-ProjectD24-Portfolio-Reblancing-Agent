# Consolidates trigger outputs.

PRIORITY = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0}

def consolidate(triggers):
    if not triggers:
        return None
    return max(triggers, key=lambda x: PRIORITY.get(x["priority"], 0))
