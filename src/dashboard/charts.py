# Plotly chart builders.

import plotly.express as px

def drift_by_category(drift_df):
    grouped = drift_df.groupby("risk_category", as_index=False)["max_drift"].mean()
    return px.bar(grouped, x="risk_category", y="max_drift", title="Average Maximum Drift")
