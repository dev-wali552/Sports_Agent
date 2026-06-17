# 🏏🏐🥎Sports Agent — AI-Powered Multi-Agent Sports Journalist🤾‍♂️🏅

A multi-agent system built with **LangGraph** that takes any sports query and automatically researches the web, then writes a clean article — all powered by **Groq's Llama 3.1** and served through a **FastAPI** backend.

**LIVE DEMO: [https://tiny-griffin-dfc226.netlify.app](https://tiny-griffin-dfc226.netlify.app)**

**API: [https://sports-agent-2k73.onrender.com/](https://sports-agent-2k73.onrender.com/)**

---

## What It Does

Ask it anything sports-related. The system spins up a pipeline of AI agents that work together:

1. A **Supervisor** decides who should act next
2. A **Researcher** searches the web for real, up-to-date sports data
3. A **Writer** turns that research into a clean, readable article
4. The Supervisor reviews the result and either loops back or finishes

The whole pipeline is stateful — it remembers conversation history per session.

---

## Architecture

```
User Query
    │
    ▼
┌─────────────┐
│  Supervisor  │  ◄─────────────────────────┐
│  (routes)    │                             │
└──────┬───────┘                             │
       │                                     │
   ┌───┴───┐                                 │
   │       │                                 │
   ▼       ▼                                 │
Researcher  Writer ──────────────────────────┘
   │
   ▼
Tavily Search Tool
   │
   └──► back to Researcher ──► Supervisor
```

The Supervisor uses **structured output** (Pydantic) to make routing decisions — it always returns one of: `researcher`, `writer`, or `FINISH`.

See [ARCHITECTURE.md](ARCHITECTURE.md) for a full breakdown of each file.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | LangGraph |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Web Search | Tavily Search API |
| API Server | FastAPI |
| Memory | LangGraph MemorySaver (in-memory) |
| Validation | Pydantic |

---

## Project Structure

```
SPORTS_AGENT/
├── state.py        # Shared state definition (messages + routing key)
├── supervisor.py   # Routing agent — decides who acts next
├── agents.py       # Researcher and Writer agents
├── graph.py        # LangGraph graph — wires everything together
├── api.py          # FastAPI server — exposes /chat endpoint
├── requirements.txt
└── runtime.txt
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MAGUIRE-GOATED/SPORTS_AGENT.git
cd SPORTS_AGENT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run the server

```bash
uvicorn api:app --reload
```

Server starts at `http://localhost:8000`

---

## API Reference

### `GET /`
Health check.

```json
{ "message": "Sports Agent API is running" }
```

### `POST /chat`
Send a sports query and get a researched article back.

**Request body:**
```json
{
  "message": "What happened in the Champions League final?",
  "session_id": "user-123"
}
```

**Response:**
```json
{
  "response": "The Champions League final..."
}
```

The `session_id` maintains conversation memory — each unique ID gets its own isolated context.

---

## How the Agents Work

**Supervisor** (`supervisor.py`)
Uses `llm.with_structured_output()` to always return a clean routing decision. No ambiguity — it's either `researcher`, `writer`, or `FINISH`.

**Researcher** (`agents.py`)
Bound to the Tavily search tool. When it needs to look something up, it emits tool calls which get handled by the `ToolNode` and routed back to it automatically.

**Writer** (`agents.py`)
Receives the full message history (including research results) and synthesizes a clean article. No tools — just pure generation.

**Graph** (`graph.py`)
Built with `StateGraph`, compiled with `MemorySaver` for per-session conversation tracking via `thread_id`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key from [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | API key from [tavily.com](https://tavily.com) |

---

## Deployment
- **Backend** — Render (free tier). `runtime.txt` pins the Python version. Auto-deploys on push to `main`. Note: free instances sleep after inactivity — first request after idle takes ~50s.
- **Frontend** — Netlify (drag and drop `index.html`). CORS is scoped to the Netlify URL in `api.py`.
