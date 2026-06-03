from state import State
from typing import Literal
from pydantic import BaseModel
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant")
class RouteDecision(BaseModel):
    next: Literal["researcher", "writer", "FINISH"]

async def supervisor(state: State) -> dict:
    system_prompt = """You are a supervisor managing two workers:
    - researcher: searches for sports information and data
    - writer: writes articles based on research
    
    Given the conversation, decide who should act next.
    If research has been done and article is written, respond FINISH.
    """
    
    supervisor_llm = llm.with_structured_output(RouteDecision)
    
    response = await supervisor_llm.ainvoke(
        [{"role": "system", "content": system_prompt}, *state["messages"]]
    )
    
    return {"next": response.next}