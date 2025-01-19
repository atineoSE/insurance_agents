import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

logger = logging.getLogger(__name__)


class VectorStore:
    """
    A class representing a vector store for storing and searching documents.

    This class uses OpenAI embeddings and PGVector to store and search documents in a PostgreSQL database.
    """

    def __init__(self):
        """
        Initializes a VectorStore instance.

        This method sets up the connection to the PostgreSQL database and initializes the vector store.
        It requires the NEON_CONNECTION_STRING environment variable to be set.

        Raises:
            ValueError: If the NEON_CONNECTION_STRING environment variable is not set.
        """
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
        """
        Adds a list of documents to the vector store.

        Args:
            documents (List[Document]): The list of documents to add.
        """
        logger.info(f"Adding {len(documents)} documents to vector store")
        self.vector_store.add_documents(
            documents, ids=[doc.metadata["source"] for doc in documents]
        )

    def has_record(self, id: str) -> bool:
        """
        Checks if a document with the given ID exists in the vector store.

        Args:
            id (str): The ID of the document to check.

        Returns:
            bool: True if the document exists, False otherwise.
        """
        return len(self.vector_store.get_by_ids([id])) > 0

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Performs a similarity search for the given query.

        Args:
            query (str): The query to search for.
            k (int, optional): The number of results to return. Defaults to 4.

        Returns:
            List[Document]: The list of matching documents.
        """
        logger.info(f"Performing similarity search for: {query}")
        matches = self.vector_store.similarity_search(query, k=k)
        logger.info(f"Retrieved {len(matches)} matches for query {query}")
        return matches
