import logging
from typing import Any, Dict, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document

from src.agents.vector_store import VectorStore

logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def load_document(self, file_path: str) -> List[Document]:
        logger.info(f"Loading document at {file_path}")
        loader = UnstructuredHTMLLoader(file_path)
        documents = loader.load()
        logger.debug(f"Extracted {len(documents)} document(s) from file {file_path}")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        logger.info(f"Processing {len(documents)} document(s)")
        split_documents = self.text_splitter.split_documents(documents)
        logger.debug(f"Split input documents into {len(split_documents)} document(s).")
        logger.debug(
            f"First document: \n{split_documents[0] if len(split_documents) > 0 else "N/A"}"
        )
        return split_documents

    def process(self, file_path: str):
        if self.vector_store.has_record(file_path):
            logger.debug(f"Record for document at {file_path} already found. Skipping.")
            return
        documents = self.load_document(file_path)
        split_documents = self.split_documents(documents)
        self.vector_store.add_documents(split_documents)
