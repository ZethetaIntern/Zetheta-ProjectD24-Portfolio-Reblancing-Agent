# Score explanation completeness without calling an LLM.

REQUIRED = ["trigger", "drift", "turnover", "cost"]

def score(text):
    text = str(text).lower()
    hits = sum(1 for term in REQUIRED if term in text)
    return {"score": hits / len(REQUIRED), "covered": hits, "total": len(REQUIRED)}
