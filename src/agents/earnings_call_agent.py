import logging

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.agents.agent_state import AgentState
from src.agents.prompts import (
    earnings_call_agent_system_prompt,
    earnings_call_agent_user_prompt,
)
from src.agents.simple_store import SimpleStore

logger = logging.getLogger(__name__)


class EarningsCallAgent:
    def __init__(self, earning_calls_store: SimpleStore):
        self.earnings_call_store = earning_calls_store
        self.llm = ChatOpenAI(temperature=0.8)

        # Initialize tools
        self.tools = self._create_tools()

        # Initialize agent
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", earnings_call_agent_system_prompt),
                ("human", earnings_call_agent_user_prompt),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        self.agent = create_openai_tools_agent(self.llm, self.tools, prompt_template)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            return_intermediate_steps=True,
        )

    def _create_tools(self) -> list[Tool]:
        tools = [
            Tool(
                name="fetch_previous_earnings_calls",
                func=self.earnings_call_store.get_records,
                description="Find relevant earnings call data from previous sessions",
            ),
        ]
        return tools

    def run(self, state: AgentState) -> AgentState:
        logger.info(f"Running earnings call agent with input state: {state}")
        output = self.agent_executor.invoke(
            {
                "market_analysis": state["market_analysis"],
                "risk_assessment": state["risk_assessment"],
            }
        )
        logger.debug(f"Got output: {output}")
        state["history"].append("earnings_call_agent")
        state["earnings_call_report"] = output["output"]
        return state
