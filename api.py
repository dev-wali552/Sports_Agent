from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import graph
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,  #javascript on one domain cannot talk to the server of another domain (same origin poilicy)
                     #without course middleware our api on render cannot talk to the frontend on netlify
    allow_origins=["https://tiny-griffin-dfc226.netlify.app/"],   # lock this down to the frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id : str

@app.get("/")
def root():
    return {"message": "Sports Agent API is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    result = await graph.ainvoke({
        "messages": [HumanMessage(content=request.message)]
    },
    config=config)
    response = result["messages"][-1].content
    return {"response": response}