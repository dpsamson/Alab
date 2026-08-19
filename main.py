from fastapi import FastAPI
from pydantic import BaseModel
import ollama
from tools import tools, available_functions #Gets all tool functions from tools folder

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat") #POST endpoint for chat requests
def chat(request: ChatRequest):
    messages = [{"role":"user","content":request.message}]

    response = ollama.chat(
        model = "qwen2.5:7b",
        messages = messages,
        tools = tools
    )
    message =  response["message"]

    if message.get("tool_calls"):
        for tool_call in message["tool_calls"]:
            func_name = tool_call["function"]["name"]
            func = available_functions[func_name]
            args = tool_call["function"].get("arguments", {})
            result = func(**args)

            messages.append(message)
            messages.append({
                "role":"tool",
                "content":str(result)
            })

        final_response = ollama.chat(model="qwen2.5:7b", messages=messages)
        return {"reply": final_response["message"]["content"]}

    return {"reply": message["content"]}
