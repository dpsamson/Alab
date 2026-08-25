from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import ollama
from tools import tools, available_functions # Gets all tool functions from tools folder
from tools.transcribe import transcribe_audio
from tools.speak import text_to_speech
import shutil

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

def process_chat(user_message: str):
    messages = [
        {"role": "system", "content": "You have access to memory tools. Whenever the user asks about themselves, ALWAYS call recall_memory first. If the user shares personal information (name, preferences, ongoing projects) without explicitly saying 'remember', proactively save it using save_memory. Use list_memories if the user asks what you know about them."},
        {"role": "user", "content": user_message}
    ]
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
        return final_response["message"]["content"]

    return message["content"]

@app.post("/chat")
def chat(request:ChatRequest):
    reply = process_chat(request.message)
    return {"reply": reply}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File (...)):
    temp_path = f"temp_{file.filename}"
    with open (temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(temp_path)
    return{"text":text}

@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcribed_text = transcribe_audio(temp_path)
    reply = process_chat(transcribed_text)
    audio_path = text_to_speech(reply)

    return FileResponse(audio_path, media_type = "audio/wav", filename = "response.wav")