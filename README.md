## Alab -  Personal AI Assistant
Alab is a personal AI assistant running an agentic tool-calling system. It is capable of deciding what appropriate tool is the best rather than specifically following a prompt mentioning the tool. Alab works alongside you instead of solely working for you. It runs on a local LLM through Ollama. Currently, Alab is equipped with tools to tell the time, perform calculations, read and write files, and search the web on its own. 

## Why I built this
The name Alab represents the developer's long-standing interest and passion for AI assistants, ignited by Jarvis's first appearance in Iron Man along with Spider-Man's EV and Friday. As a Computer Engineering student taking the AI elective, building my own personal AI assistant seemed like the best way to deepen my understanding while creating something I could use as a foundation for future projects. 

## Current Capabilities
- Tool-calling agentic loop (local LLM via Ollama)
- Tools: time, calculator, file read/write, web search

## Tech Stack
- Ollama (qwen2.5:7b)
- FastAPI
- Python

## How to Run
1. Clone the repo
2. Create and activate a virtual environment:
   `python -m venv venv`
   `.\venv\Scripts\Activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Install Ollama and pull the model: `ollama pull qwen2.5:7b`
5. Create a `.env` file with your Tavily API key: `TAVILY_API_KEY=your_key_here`
6. Run the server: `uvicorn main:app --reload`
7. Send a test request to `POST http://127.0.0.1:8000/chat` with a JSON body: `{"message": "your message here"}`


## Roadmap
- [x] Phase 1: Core tool-calling backbone
- [ ] Phase 2: Voice (Whisper + TTS)
- [ ] Phase 3: Persistent memory
- [ ] Phase 4: Domain-specific tools

