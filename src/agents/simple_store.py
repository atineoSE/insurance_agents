import logging

from src.agents.earnings_call_data import (
    earnings_call_01,
    earnings_call_02,
    earnings_call_03,
)

logger = logging.getLogger(__name__)


class SimpleStore:
    """
    A simple store class for storing and retrieving earnings call reports.

    This class is used for illustrative purposes and stores reports in memory.
    In a real-world application, this would likely be replaced with a database or other persistent storage.
    """

    def __init__(self):
        """
        Initializes a SimpleStore instance.

        This method sets up the store with a hardcoded list of earnings call reports.
        """
        # Hardcoded from static data for illustrative purposes
        self.reports = [earnings_call_01, earnings_call_02, earnings_call_03]

    def get_records(self, context: str) -> list[str]:
        """
        Retrieves a list of earnings call reports from the store.

        Args:
            context (str): The context for which to retrieve reports. This is currently not used in this implementation.

        Returns:
            list[str]: A list of earnings call reports. In this toy example, all reports are returned.
        """
        logger.info(f"Retrieving simple store records for context: {context}")
        # Return all in this toy example
        return self.reports
