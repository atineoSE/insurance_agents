import operator
from typing import Annotated

from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    A typed dictionary representing the state of an agent.

    This dictionary contains the following keys:
        - query: The analysis query being executed.
        - market_analysis: The market analysis report.
        - risk_assessment: The risk assessment report.
        - earnings_call_report: The earnings call report.
        - history: A list of previous states.

    Note: The use of Annotated with operator.add is as documented here:
    https://langchain-ai.github.io/langgraph/how-tos/branching/#parallel-node-fan-out-and-fan-in
    """

    query: Annotated[str, operator.add]
    market_analysis: Annotated[str, operator.add]
    risk_assessment: Annotated[str, operator.add]
    earnings_call_report: Annotated[str, operator.add]
    history: Annotated[list[str], operator.add]
