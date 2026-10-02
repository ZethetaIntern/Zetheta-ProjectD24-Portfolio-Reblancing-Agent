# Automated quarterly audit over a sample of decisions.

class ComplianceAuditor:
    def audit(self, decisions):
        total = len(decisions)
        passed = sum(bool(d.get("compliance", {}).get("passed", False)) for d in decisions)
        return {
            "sample_size": total,
            "compliance_pass_rate": passed / total if total else 1.0,
            "all_have_audit_record": all("portfolio_id" in d for d in decisions),
        }
