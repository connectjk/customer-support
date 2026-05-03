"""FastAPI entry point for customer-support (Self-Hosted on Azure Container Apps)."""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

from .agent_runtime import run_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting customer-support...")
    yield
    print("Shutting down customer-support...")


app = FastAPI(
    title="customer-support",
    description="A customer support agent that can search a knowledge base, create support tickets, track ticket status, and escalate complex issues.",
    version="1.0.0",
    lifespan=lifespan,
)


class InvokeRequest(BaseModel):
    message: str
    session_id: str | None = None


class InvokeResponse(BaseModel):
    response: str
    session_id: str | None = None


@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "customer-support"}


@app.post("/invoke", response_model=InvokeResponse)
async def invoke(req: InvokeRequest):
    """Invoke the agent with a message."""
    try:
        result = await run_agent(req.message)
        return InvokeResponse(response=result, session_id=req.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))