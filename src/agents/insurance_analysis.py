import logging

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.agents.agent_state import AgentState
from src.agents.prompts import (
    insurance_agent_system_prompt,
    insurance_agent_user_prompt,
)
from src.agents.vector_store import VectorStore

logger = logging.getLogger(__name__)


class InsuranceAnalysisAgent:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(temperature=0)

        # Initialize tools
        self.tools = self._create_tools()

        # Initialize agent
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", insurance_agent_system_prompt),
                ("human", insurance_agent_user_prompt),
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
                name="search_documents",
                func=self.vector_store.similarity_search,
                description="Search through insurance documents",
            ),
        ]
        return tools

    def run(self, state: AgentState) -> AgentState:
        logger.info(f"Running insurance agent with input state: {state}")
        output = self.agent_executor.invoke(
            {
                "documents": "",
                "query": state["query"],
            }
        )
        logger.debug(f"Got output: {output}")
        state["history"].append("insurance_agent")
        state["output"] = output["output"]
        return state
