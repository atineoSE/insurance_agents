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
            documents, ids=[doc.metadata["source"] for doc in documents]
        )

    def has_record(self, id: str) -> bool:
        return len(self.vector_store.get_by_ids([id])) > 0

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        logger.info(f"Performing similarity search for: {query}")
        matches = self.vector_store.similarity_search(query, k=k)
        logger.info(f"Retrieved {len(matches)} matches for query {query}")
        return matches
