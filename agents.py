from dotenv import load_dotenv
load_dotenv()
import os
from state import State
from typing import List , Dict , cast
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from datetime import datetime , UTC
from langchain_community.tools.tavily_search import TavilySearchResults

llm = ChatGroq(model="llama-3.3-70b-versatile")
tavily = TavilySearchResults(max_results = 2)


async def researcher(state:State) -> Dict[str,List[AIMessage]] :


    
    model = llm.bind_tools([tavily])
    system_prompt = """You are a Sports Researcher. On a given topic search for relevant and unbiased info. SYSTEM_TIME={system_time}"""
    system_message = system_prompt.format(
        system_time = datetime.now(tz = UTC).isoformat()
    )
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state["messages"]]
        ),
    )
    return {"messages": [response]}

async def writer(state:State)-> Dict[str,List[AIMessage]] :
    system_prompt = "you are a sports writer, write a clean article from the research.SYSTEM_TIME={system_time}"
    system_message = system_prompt.format(
        system_time = datetime.now(tz = UTC).isoformat()
    )
    response = cast(
        AIMessage,
        await llm.ainvoke(
            [{"role": "system", "content": system_message}, *state["messages"]]
        ),
    )
    return {"messages": [response]}









    

