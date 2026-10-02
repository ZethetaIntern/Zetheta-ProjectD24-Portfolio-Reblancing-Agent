# ADR-001: Gradio instead of Streamlit

## Context
The project specification recommends Streamlit, but the requested user interface is Gradio.

## Decision
Use Gradio for the dashboard while preserving the source's five logical views.

## Consequence
The repository is directly aligned with the user's UI requirement while keeping
the underlying service and module architecture independent from the UI.
