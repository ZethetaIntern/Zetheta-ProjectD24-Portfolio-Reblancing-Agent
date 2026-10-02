# Escalation when autonomous processing cannot satisfy constraints.

def escalate(reason, attempts):
    return {
        "escalated": True,
        "reason": reason,
        "attempts": attempts,
        "requires_human_review": True,
    }
