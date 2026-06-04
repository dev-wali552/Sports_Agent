from state import State
from typing import Literal
from pydantic import BaseModel
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant")
class RouteDecision(BaseModel):
    next: Literal["researcher", "writer", "FINISH"]

async def supervisor(state: State) -> dict:
    messages = state["messages"]
    
    # count what's already happened
    has_research = any(
        hasattr(m, 'tool_calls') and m.tool_calls 
        for m in messages
    )
    has_article = len([m for m in messages if hasattr(m, 'content') and m.content and len(m.content) > 200]) > 1

    if not has_research:
        return {"next": "researcher"}
    elif not has_article:
        return {"next": "writer"}
    else:
        return {"next": "FINISH"}