"""FastAPI backend for the dashboard chatbot."""

import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils import handle_query


app = FastAPI(title="TrailEdge GenAI Chatbot API")


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return handle_query(request.query)
