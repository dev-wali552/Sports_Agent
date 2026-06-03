from typing import Annotated, Sequence
from typing_extensions import Annotated ,TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


class State(TypedDict):    
    messages: Annotated[Sequence[AnyMessage], add_messages]
    next: str                                                  # supervisor sets this to "researcher", "writer", or "FINISH"


