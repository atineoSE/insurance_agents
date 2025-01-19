import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.documents import Document

from src.agents.vector_store import VectorStore

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    A class responsible for processing documents and adding them to a vector store.

    This class loads documents from files, splits them into smaller chunks, and adds them to a vector store.
    It also checks if a document has already been processed before attempting to process it again.
    """

    def __init__(self, vector_store: VectorStore):
        """
        Initializes a DocumentProcessor instance.

        Args:
            vector_store (VectorStore): The vector store where the processed documents will be added.
        """
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )

    def load_document(self, file_path: str) -> list[Document]:
        """
        Loads a document from a file.

        Args:
            file_path (str): The path to the file containing the document.

        Returns:
            list[Document]: A list of documents extracted from the file.
        """
        logger.info(f"Loading document at {file_path}")
        loader = UnstructuredHTMLLoader(file_path)
        documents = loader.load()
        logger.debug(f"Extracted {len(documents)} document(s) from file {file_path}")
        return documents

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Splits a list of documents into smaller chunks.

        Args:
            documents (list[Document]): The list of documents to be split.

        Returns:
            list[Document]: The list of split documents.
        """
        logger.info(f"Processing {len(documents)} document(s)")
        split_documents = self.text_splitter.split_documents(documents)
        logger.debug(f"Split input documents into {len(split_documents)} document(s).")
        logger.debug(
            f"First document: \n{split_documents[0] if len(split_documents) > 0 else 'N/A'}"
        )
        return split_documents

    def process(self, file_path: str):
        """
        Processes a document at the given file path and adds it to the vector store.

        If the document has already been processed, this method does nothing.

        Args:
            file_path (str): The path to the file containing the document to be processed.
        """
        if self.vector_store.has_record(file_path):
            logger.debug(f"Record for document at {file_path} already found. Skipping.")
            return
        documents = self.load_document(file_path)
        split_documents = self.split_documents(documents)
        self.vector_store.add_documents(split_documents)
