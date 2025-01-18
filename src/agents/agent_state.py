from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    query: str
    output: str | None
    history: list[str]
