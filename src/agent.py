#!/usr/bin/env python3

import argparse
import logging
import os
from typing import Annotated, Dict, TypedDict

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.agents import AgentFinish
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, START, Graph, StateGraph
from typing_extensions import TypedDict

from agents.document_processor import DocumentProcessor
from agents.insurance_analysis import InsuranceAnalysisAgent
from agents.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: list[BaseMessage]
    history: list[str]


def supervisor_function(state: AgentState) -> AgentState:
    logger.info(f"Running supervisor with input state: {state}")
    state["history"].append("supervisor_function")
    return state


def create_agent_graph(vector_store: VectorStore) -> Graph:
    # analysis_agent = InsuranceAnalysisAgent(vector_store)

    graph = StateGraph(AgentState)

    graph.add_node("supervisor_1", supervisor_function)
    graph.add_node("supervisor_2", supervisor_function)

    graph.add_edge(START, "supervisor_1")
    graph.add_edge("supervisor_1", "supervisor_2")
    graph.add_edge("supervisor_2", END)

    return graph.compile()


def main():
    parser = argparse.ArgumentParser(description="Insurance Data Analysis Pipeline")
    parser.add_argument(
        "--docs-dir",
        type=str,
        help="Path to directory with source documents",
        required=True,
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Analysis query to run",
        default="What's the trend in auto insurance costs over the last 3 years?",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize dependencies
    vector_store = VectorStore()
    # doc_processor = DocumentProcessor(vector_store)

    # # Load documents, if needed
    # # Note that provided documents have extension XLS but are actually HTML
    # source_files = [f for f in os.listdir(args.docs_dir) if f.endswith(".xls")]
    # logger.info(f"Found {len(source_files)} source files at {args.docs_dir}")
    # for source_file in source_files:
    #     source_file_path = os.path.join(args.docs_dir, source_file)
    #     doc_processor.process(source_file_path)

    # Create the agent graph
    graph = create_agent_graph(vector_store)

    # Initialize the state
    initial_state = AgentState(messages=[HumanMessage(content=args.query)], history=[])

    # Run the graph
    for output in graph.stream(initial_state):
        if "__end__" not in output:
            logger.info(f"Intermediate output: {output}")

    logger.info("Analysis complete!")


if __name__ == "__main__":
    main()
