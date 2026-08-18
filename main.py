from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = ollama.chat(
        model = "qwen2.5:7b",
        messages = [
            {"role":"user", "content":request.message}
        ]
    )
    return {"reply":response["message"]["content"]}
