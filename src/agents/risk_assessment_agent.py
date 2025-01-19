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
    """
    A class representing a risk assessment agent.

    This agent is responsible for generating a risk assessment report based on the input query.
    It uses a language model to generate the report.
    """

    def __init__(self):
        """
        Initializes a RiskAssessmenttAgent instance.

        This method sets up the language model and the prompt template used by the agent.
        """
        self.llm = ChatOpenAI(temperature=0)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", risk_assessment_system_prompt),
                ("human", risk_assessment_user_prompt),
            ]
        )

    def run(self, state: AgentState) -> AgentState:
        """
        Runs the risk assessment agent with the given input state.

        The agent generates a risk assessment report based on the input query in the state.
        The report is then added to the output state, along with the current agent's name in the history.

        Args:
            state (AgentState): The input state.

        Returns:
            AgentState: The output state with the risk assessment report.

        Note: The agent's name in the history is currently hardcoded as "risk_management_agent",
              which does not match the class name "RiskAssessmenttAgent". This might be a typo.
        """
        logger.info(f"Running risk assessment agent with input state: {state}")
        prompt = self.prompt_template.invoke({"query": state["query"]})
        output = self.llm.invoke(prompt)
        logger.debug(f"Got output: {output}")
        state["history"].append("risk_assessment_agent")
        state["risk_assessment"] = output.content
        return state
