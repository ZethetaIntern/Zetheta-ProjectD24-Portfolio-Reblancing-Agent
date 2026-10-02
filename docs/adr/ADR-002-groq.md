# ADR-002: Groq for language generation

## Decision
Use Groq as the LLM provider for explanation generation.

## Reason
The user explicitly requested Groq. Numerical calculations remain deterministic
so the LLM cannot silently change portfolio mathematics.
