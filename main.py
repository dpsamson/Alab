from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import ollama
from tools import tools, available_functions # Gets all tool functions from tools folder
from tools.transcribe import transcribe_audio
import shutil

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/transcribe")
async def transcribe(file: UploadFile = File (...)):
    temp_path = f"temp_{file.filename}"
    with open (temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(temp_path)
    return{"text":text}

@app.post("/chat") # POST endpoint for chat requests
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
