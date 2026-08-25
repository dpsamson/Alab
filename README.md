## Alab -  Personal AI Assistant
Alab is a personal AI assistant running an agentic tool-calling system. It is capable of deciding what appropriate tool is the best rather than specifically following a prompt mentioning the tool. Alab works alongside you instead of solely working for you. It runs on a local LLM through Ollama. Currently, Alab is equipped with tools to tell the time, perform calculations, read and write files, and search the web on its own. 

## Why I built this
The name Alab represents the developer's long-standing interest and passion for AI assistants, ignited by Jarvis's first appearance in Iron Man along with Spider-Man's EV and Friday. As a Computer Engineering student taking the AI elective, building my own personal AI assistant seemed like the best way to deepen my understanding while creating something I could use as a foundation for future projects. 

## Current Capabilities
- Tool-calling agentic loop (local LLM via Ollama)
- Tools: time, calculator, file read/write, web search
- Voice input (speech-to-text via Whisper)
- Voice output (text-to-speech)
- Full voice conversation loop: speak a request, get a spoken reply
- Persistent memory: saves and recalls facts across sessions (SQLite), with proactive save/recall via system prompt guidance

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
4. Install ffmpeg (required for Whisper) — e.g. `winget install ffmpeg` on Windows
5. Install Ollama and pull the model: `ollama pull qwen2.5:7b`
6. Create a `.env` file with your Tavily API key: `TAVILY_API_KEY=your_key_here`
7. Run the server: `uvicorn main:app --reload`
8. Test endpoints:
   - `POST /chat` with JSON `{"message": "your message"}`
   - `POST /transcribe` with an audio file
   - `POST /voice-chat` with an audio file (full voice loop)

## Known Issues
- Occasional CUDA crash when testing, specifically if Ollama is started via windows startup apps
- Local models (qwen2.5:7b) don't reliably call tools proactively without explicit system prompt guidance — fixed for memory tools via an explicit system prompt instructing when to check/save memory.

## Roadmap
- [x] Phase 1: Core tool-calling backbone
- [x] Phase 2: Voice (Whisper + TTS)
- [x] Phase 3: Persistent memory
- [ ] Phase 4: Domain-specific tools

