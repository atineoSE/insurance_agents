import logging
from typing import Any, Dict, List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def load_excel(self, file_path: str) -> List[Document]:
        """
        Load Excel file using UnstructuredExcelLoader

        Args:
            file_path: Path to the Excel file

        Returns:
            List of Document objects
        """
        logger.info(f"Loading Excel file: {file_path}")
        loader = UnstructuredExcelLoader(file_path)
        documents = loader.load()
        logger.debug(f"Extracted {len(documents)} documents from file {file_path}")
        return documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process documents by splitting and extracting metadata

        Args:
            documents: List of raw documents

        Returns:
            List of processed Document objects
        """
        logger.info(f"Processing {len(documents)} documents")
        split_documents = self.text_splitter.split_documents(documents)
        logger.debug(f"Split input documents into {len(split_documents)} documents.")
        logger.debug(
            f"First document: \n{split_documents[0] if len(split_documents) > 0 else "N/A"}"
        )
        return split_documents

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent function to be called by the supervisor

        Args:
            state: Current state of the system

        Returns:
            Updated state
        """

        if (file_path := state["file_path"]) is None:
            raise ValueError("Missing file path for documents")

        documents = self.load_excel(file_path)
        split_documents = self.process_documents(documents)
        state["documents"] = split_documents

        return state
