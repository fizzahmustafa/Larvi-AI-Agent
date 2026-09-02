from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents.master_agent import process_request


app = FastAPI(
    title="Larvi AI Assistant",
    description="Autonomous Email and Calendar AI Agent"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Larvi is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = process_request(request.message)

        return {
            "success": True,
            "response": result
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }