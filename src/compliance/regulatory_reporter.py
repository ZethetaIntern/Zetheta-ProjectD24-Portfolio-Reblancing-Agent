# Produce a simple regulatory-style audit summary.

def generate(audit):
    return (
        "Quarterly Compliance Report\n"
        f"Sample size: {audit['sample_size']}\n"
        f"Compliance pass rate: {audit['compliance_pass_rate']:.2%}\n"
        f"Audit records complete: {audit['all_have_audit_record']}\n"
    )
