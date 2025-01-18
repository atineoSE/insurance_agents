from typing_extensions import TypedDict


class AgentState(TypedDict):
    query: str
    market_analysis: str | None
    earnings_call_report: str | None
    history: list[str]
