import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.agents.agent_state import AgentState
from src.agents.prompts import (
    risk_assessment_system_prompt,
    risk_assessment_user_prompt,
)

logger = logging.getLogger(__name__)


class RiskAssessmenttAgent:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", risk_assessment_system_prompt),
                ("human", risk_assessment_user_prompt),
            ]
        )

    def run(self, state: AgentState) -> AgentState:
        logger.info(f"Running risk assessment agent with input state: {state}")
        prompt = self.prompt_template.invoke({"query": state["query"]})
        output = self.llm.invoke(prompt)
        logger.debug(f"Got output: {output}")
        state["history"].append("risk_management_agent")
        state["risk_assessment"] = output.content
        return state
