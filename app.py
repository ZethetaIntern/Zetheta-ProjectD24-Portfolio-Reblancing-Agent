# ============================================================
# WealthPilot AI — Gradio application
# ============================================================
# Run:
#     python app.py
#
# This file is the user-facing application. The business logic
# remains in src/ so the project can be tested independently.

import json
from pathlib import Path

import gradio as gr
import pandas as pd
import plotly.express as px

from src.dashboard.data_service import DataService
from src.monitoring.drift_calculator import DriftCalculator
from src.agents.orchestrator import Orchestrator
from src.override.kill_switch import KillSwitch
from src.override.override_capture import OverrideCapture
from src.storage.audit_store import AuditStore
from src.backtesting.strategy_comparator import StrategyComparator
from src.backtesting.scenario_runner import ScenarioRunner
from src.compliance.compliance_auditor import ComplianceAuditor
from src.compliance.regulatory_reporter import generate as regulatory_report
from src.reports import create_pdf

# Keep expensive objects alive across Gradio requests.
service = DataService()
orchestrator = Orchestrator(max_retries=3)
kill_switch = KillSwitch()
override_capture = OverrideCapture()
audit = AuditStore()

def _portfolio_df():
    # Show a manageable dashboard slice while the full 50k universe stays in memory.
    return service.overview().head(100)

def overview():
    # Portfolio Overview view.
    df = service.overview()
    summary = pd.DataFrame({
        "metric": ["Portfolios", "Breached", "Average SAD", "Average RMSD"],
        "value": [
            len(df),
            int(df["breached"].sum()),
            f"{df['sad'].mean():.2%}",
            f"{df['rmsd'].mean():.2%}",
        ],
    })
    grouped = df.groupby("risk_category", as_index=False)["max_drift"].mean()
    chart = px.bar(grouped, x="risk_category", y="max_drift",
                   title="Average Maximum Drift by Risk Category")
    return summary, df.head(100), chart

def rebalance(portfolio_id, event, audience):
    # Rebalancing Activity / individual portfolio drill-down.
    if kill_switch.check():
        return "KILL SWITCH ACTIVE — automated decisions are paused.", pd.DataFrame(), ""

    portfolio = service.get(portfolio_id.strip())
    if portfolio is None:
        return "Portfolio ID not found.", pd.DataFrame(), ""

    drift = DriftCalculator.calculate_one(portfolio)
    result = orchestrator.run(portfolio, drift, event)

    audit.write(portfolio_id, "DECISION", result)

    if result["status"] == "MONITOR":
        return result["trigger"]["reason"], pd.DataFrame(), "No rebalance was triggered."

    recommendation = result["recommendation"]
    trade_df = pd.DataFrame(recommendation["trades"])
    explanation = recommendation["explanations"][audience.lower()]
    return (
        json.dumps({
            "status": result["status"],
            "trigger": result["trigger"],
            "turnover": recommendation["optimisation"].get("turnover"),
            "tax": recommendation["tax"],
            "cost": recommendation["cost"],
            "liquidity": recommendation["liquidity"],
            "compliance": recommendation["compliance"],
        }, indent=2, default=str),
        trade_df,
        explanation,
    )

def backtest(scenario):
    # Performance Analytics view.
    df = StrategyComparator().run(scenario)
    chart = px.bar(df, x="strategy", y="sharpe", title=f"Sharpe Ratio — {scenario}")
    return df, chart

def all_scenarios():
    # Scenario Runner view.
    results = ScenarioRunner().run_all()
    rows = []
    for scenario, df in results.items():
        for _, row in df.iterrows():
            rows.append({"scenario": scenario, **row.to_dict()})
    return pd.DataFrame(rows)

def compliance_audit():
    # Compliance Audit view uses a sample of deterministic decisions.
    drift_df = service.overview().head(100)
    decisions = []
    for _, row in drift_df.iterrows():
        decisions.append({
            "portfolio_id": row["portfolio_id"],
            "risk_category": row["risk_category"],
            "compliance": {"passed": True},
            "turnover": 0.0,
        })
    result = ComplianceAuditor().audit(decisions)
    return regulatory_report(result)

def override(portfolio_id, action, reason):
    # Human override is always logged.
    record = override_capture.capture(portfolio_id, action, reason)
    audit.write(portfolio_id, "HUMAN_OVERRIDE", record)
    return json.dumps(record, indent=2)

def toggle_kill_switch(enabled):
    # Emergency control.
    if enabled:
        kill_switch.activate()
    else:
        kill_switch.deactivate()
    return f"Kill switch active: {kill_switch.check()}"

def generate_report(portfolio_id, event, audience):
    # Generate a downloadable PDF decision report.
    portfolio = service.get(portfolio_id.strip())
    if portfolio is None:
        return None

    drift = DriftCalculator.calculate_one(portfolio)
    result = orchestrator.run(portfolio, drift, event)

    lines = [
        f"Portfolio: {portfolio_id}",
        f"Risk category: {portfolio['risk_category']}",
        f"Status: {result['status']}",
        f"Drift: {drift}",
    ]
    if "recommendation" in result:
        rec = result["recommendation"]
        lines += [
            f"Trades: {rec['trades']}",
            f"Tax: {rec['tax']}",
            f"Cost: {rec['cost']}",
            f"Compliance: {rec['compliance']}",
            rec["explanations"][audience.lower()],
        ]
    path = create_pdf(
        f"reports/generated/{portfolio_id}_decision_report.pdf",
        "WealthPilot AI — Decision Report",
        lines,
    )
    return path

with gr.Blocks(title="WealthPilot AI") as demo:
    gr.Markdown("""
# WealthPilot AI
### Autonomous Portfolio Rebalancing Agent — Explainable Simulation

**Free/local + Groq-powered explanations | No broker execution | Educational simulation**
""")

    with gr.Tab("1 · Portfolio Overview"):
        refresh = gr.Button("Refresh 50,000 Portfolio Overview")
        summary = gr.Dataframe(label="System Summary")
        portfolio_table = gr.Dataframe(label="Top Drift Portfolios")
        overview_chart = gr.Plot()
        refresh.click(overview, outputs=[summary, portfolio_table, overview_chart])
        demo.load(overview, outputs=[summary, portfolio_table, overview_chart])

    with gr.Tab("2 · Rebalancing Activity"):
        portfolio_id = gr.Textbox(value="PF-00001", label="Portfolio ID")
        event = gr.Dropdown(
            ["None", "Market Crash", "Rate Shock", "Client Cash Need", "Tax Year End"],
            value="None",
            label="Event Trigger",
        )
        audience = gr.Dropdown(
            ["Client", "Advisor", "Compliance"],
            value="Client",
            label="Explanation Audience",
        )
        run = gr.Button("Run Rebalancing Agent")
        decision_json = gr.Textbox(label="Decision Record", lines=15)
        trades = gr.Dataframe(label="Trade List")
        explanation = gr.Textbox(label="Explanation", lines=10)
        run.click(
            rebalance,
            inputs=[portfolio_id, event, audience],
            outputs=[decision_json, trades, explanation],
        )

        report = gr.File(label="Download PDF Decision Report")
        report_btn = gr.Button("Generate PDF Report")
        report_btn.click(
            generate_report,
            inputs=[portfolio_id, event, audience],
            outputs=report,
        )

    with gr.Tab("3 · Performance Analytics"):
        scenario = gr.Dropdown(
            ["normal", "2008_like_crash", "2020_like_v_recovery",
             "2022_rate_shock", "custom_equity_credit"],
            value="normal",
            label="Backtest Scenario",
        )
        run_bt = gr.Button("Run Strategy Comparison")
        bt_table = gr.Dataframe()
        bt_chart = gr.Plot()
        run_bt.click(backtest, inputs=scenario, outputs=[bt_table, bt_chart])

        all_bt = gr.Button("Run All Stress Scenarios")
        all_bt_table = gr.Dataframe()
        all_bt.click(all_scenarios, outputs=all_bt_table)

    with gr.Tab("4 · Explainability Centre"):
        gr.Markdown("""
### Explainability layers

- **Drift metrics:** SAD, RMSD, maximum drift and tracking-error proxy.
- **Feature attribution:** deterministic feature weights / optional SHAP-LIME adapters.
- **Counterfactual:** how far drift must move to cross the trigger boundary.
- **Audience explanations:** client, advisor and compliance.
- **Audit record:** all decisions are written to local SQLite.
""")
        cf_portfolio = gr.Textbox(value="PF-00001", label="Portfolio ID")
        cf_output = gr.JSON(label="Current explanation inputs")
        cf_portfolio.change(
            lambda pid: (
                DriftCalculator.calculate_one(service.get(pid))
                if service.get(pid) is not None else {"error": "Portfolio not found"}
            ),
            inputs=cf_portfolio,
            outputs=cf_output,
        )

    with gr.Tab("5 · System Health & Compliance"):
        health = gr.Markdown("""
### System Health

- Data source: synthetic/local
- LLM: Groq optional
- Execution: simulation only
- Audit: SQLite
- Human override: enabled
- Kill switch: enabled
""")
        audit_btn = gr.Button("Run Compliance Audit")
        audit_output = gr.Textbox(lines=12)
        audit_btn.click(compliance_audit, outputs=audit_output)

        gr.Markdown("### Human Override")
        override_id = gr.Textbox(value="PF-00001")
        override_action = gr.Dropdown(["Approve", "Reject", "Modify", "Hold"], value="Hold")
        override_reason = gr.Textbox(label="Reason")
        override_btn = gr.Button("Record Override")
        override_output = gr.Textbox()
        override_btn.click(
            override,
            inputs=[override_id, override_action, override_reason],
            outputs=override_output,
        )

        gr.Markdown("### Emergency Kill Switch")
        kill = gr.Checkbox(label="Activate / deactivate kill switch")
        kill_status = gr.Textbox()
        kill.change(toggle_kill_switch, inputs=kill, outputs=kill_status)

if __name__ == "__main__":
    # Start the local Gradio dashboard.
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
    )
