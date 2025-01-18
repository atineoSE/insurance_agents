import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

# Using PGVector version as recommended here: https://python.langchain.com/docs/integrations/vectorstores/pgvector/

load_dotenv()

logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self):
        """Initialize the vector store with OpenAI embeddings and PGVector"""
        self.connection_string = os.getenv("NEON_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("NEON_CONNECTION_STRING environment variable is required")

        self.embeddings = OpenAIEmbeddings()
        self.collection_name = "insurance_docs"

        logger.info("Initializing vector store")
        self.vector_store = PGVector(
            embeddings=self.embeddings,
            collection_name=self.collection_name,
            connection=self.connection_string,
            use_jsonb=True,
        )

    def add_documents(self, documents: List[Document]):
        logger.info(f"Adding {len(documents)} documents to vector store")
        self.vector_store.add_documents(
            documents, ids=[doc.metadata["id"] for doc in documents]
        )

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        TODO: Perform similarity search

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar documents
        """
        logger.info(f"Performing similarity search for: {query}")
        # TODO: Implement similarity search
        return []

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent function to be called by the supervisor

        Args:
            state: Current state of the system

        Returns:
            Updated state
        """
        # TODO: Implement agent logic
        # Example:
        # 1. Check if there are new documents to store
        # 2. Add documents to vector store
        # 3. Update state with storage status
        return state
