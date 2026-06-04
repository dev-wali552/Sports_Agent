from state import State
from typing import Literal
from pydantic import BaseModel
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.1-8b-instant")
class RouteDecision(BaseModel):
    next: Literal["researcher", "writer", "FINISH"]

async def supervisor(state: State) -> dict:
    system_prompt = """You are a supervisor managing two workers:
        - researcher: searches for sports info using Tavily. Call ONCE only.
        - writer: writes a sports article from the research. Call ONCE only.

        Follow this STRICT order:
        1. First call: always route to researcher
        2. Second call: always route to writer  
        3. Third call: always return FINISH

        Never loop. Never call the same worker twice."""
    
    supervisor_llm = llm.with_structured_output(RouteDecision)
    
    response = await supervisor_llm.ainvoke(
        [{"role": "system", "content": system_prompt}, *state["messages"]]
    )
    
    return {"next": response.next}