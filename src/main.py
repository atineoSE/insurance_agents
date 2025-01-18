#!/usr/bin/env python3

import argparse
import logging
import os

from langgraph.graph import END, START, Graph, StateGraph

from agents.agent_state import AgentState
from agents.document_processor import DocumentProcessor
from agents.earnings_call_agent import EarningsCallAgent
from agents.insurance_analysis_agent import InsuranceAnalysisAgent
from agents.risk_assessment_agent import RiskAssessmenttAgent
from agents.simple_store import SimpleStore
from agents.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_agent_graph(vector_store: VectorStore, simple_store: SimpleStore) -> Graph:
    analysis_agent = InsuranceAnalysisAgent(vector_store)
    risk_assessment_agent = RiskAssessmenttAgent()
    earnings_call_agent = EarningsCallAgent(simple_store)

    graph = StateGraph(AgentState)

    graph.add_node("insurance_agent", analysis_agent.run)
    graph.add_node("risk_assessment_agent", risk_assessment_agent.run)
    graph.add_node("earnings_call_agent", earnings_call_agent.run)

    graph.add_edge(START, "insurance_agent")
    graph.add_edge(START, "risk_assessment_agent")
    graph.add_edge("insurance_agent", "earnings_call_agent")
    graph.add_edge("risk_assessment_agent", "earnings_call_agent")
    graph.add_edge("earnings_call_agent", END)

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
    doc_processor = DocumentProcessor(vector_store)
    simple_store = SimpleStore()

    # Load documents, if needed
    # Note that provided documents have extension XLS but are actually HTML
    source_files = [f for f in os.listdir(args.docs_dir) if f.endswith(".xls")]
    logger.info(f"Found {len(source_files)} source files at {args.docs_dir}")
    for source_file in source_files:
        source_file_path = os.path.join(args.docs_dir, source_file)
        doc_processor.process(source_file_path)

    # Create the agent graph
    graph = create_agent_graph(vector_store, simple_store)
    graph.get_graph().draw_mermaid_png(output_file_path="graph_chart.png")

    # Initialize the state
    initial_state = AgentState(
        query=args.query, market_analysis="", earnings_call_report="", history=[]
    )

    # Run the graph
    for idx, state in enumerate(graph.stream(initial_state)):
        logger.info(f"STEP {idx}: {state}")

    logger.info("Analysis complete!")

    print(f"\n\nQuery: {args.query}")
    print(f"\n\nAnswer: {state["earnings_call_agent"]["earnings_call_report"]}")


if __name__ == "__main__":
    main()
