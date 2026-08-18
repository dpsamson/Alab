from fastapi import FastAPI
from pydantic import BaseModel
import ollama
from datetime import datetime

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [{
    "type":"function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current time and date",
        "parameters":{
            "type":"object",
            "properties":{},
            "required":[]
        }
    }
}]

available_functions = {
    "get_current_time": get_current_time
}

@app.post("/chat")
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
            result = func()

            messages.append(message)
            messages.append({
                "role":"tool",
                "content":str(result)
            })

        final_response = ollama.chat(model="qwen2.5:7b", messages=messages)
        return {"reply": final_response["message"]["content"]}

    return {"reply": message["content"]}
