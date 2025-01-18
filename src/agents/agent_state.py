from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: list[BaseMessage]
    query: str
    history: list[str]
