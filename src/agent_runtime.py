"""Agent runtime - setup and run loop for customer-support."""

import os
from openai import AzureOpenAI

SYSTEM_PROMPT = """\
A customer support agent that can search a knowledge base, create support tickets, track ticket status, and escalate complex issues to human agents when needed. It responds politely, provides step-by-step troubleshooting, and always confirms resolution before closing a case.
"""

def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-06-01",
    )

async def run_agent(message: str) -> str:
    """Process a single user message and return the agent response."""
    client = _get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
        messages=messages,
    )

    return response.choices[0].message.content or ""