import logging
from typing import Any, Dict, List

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
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

        # Initialize retrieval chain
        # self.retrieval_chain = RetrievalQAWithSourcesChain.from_llm(llm=self.llm)

        # Initialize tools
        self.tools = self._create_tools()

        # Initialize agent
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", insurance_agent_system_prompt),
                # MessagesPlaceholder("chat_history", optional=True),
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

    def _create_tools(self) -> List[Tool]:
        tools = [
            Tool(
                name="search_documents",
                func=self.vector_store.similarity_search,
                description="Search through insurance documents",
            ),
            # TODO: Add more tools for analysis
        ]
        return tools

    def analyze_trends(self, query: str) -> str:
        """
        TODO: Analyze insurance trends

        Args:
            query: Analysis query

        Returns:
            Analysis results
        """
        logger.info(f"Analyzing trends for query: {query}")
        # TODO: Implement trend analysis
        return ""

    def run(self, state: AgentState) -> AgentState:
        logger.info(f"Running insurance agent with input state: {state}")
        output = self.agent_executor.invoke(
            {
                # "chat_history": state["messages"],
                "documents": "",
                "query": state["query"],
            }
        )
        logger.info(f"Got output: {output}")
        state["history"].append("insurance_agent")
        return state
