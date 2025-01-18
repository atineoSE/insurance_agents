import operator
from typing import Annotated

from typing_extensions import TypedDict


class AgentState(TypedDict):
    query: Annotated[str, operator.add]
    market_analysis: Annotated[str, operator.add]
    risk_assessment: Annotated[str, operator.add]
    earnings_call_report: Annotated[str, operator.add]
    history: Annotated[list[str], operator.add]
