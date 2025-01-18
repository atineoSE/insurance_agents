import logging

from src.agents.earnings_call_data import (
    earnings_call_01,
    earnings_call_02,
    earnings_call_03,
)

logger = logging.getLogger(__name__)


class SimpleStore:
    reports: list[str]

    def __init__(self):
        # Hardcoded from static data for illustrative purposes
        self.reports = [earnings_call_01, earnings_call_02, earnings_call_03]

    def get_records(self, context: str) -> list[str]:
        logger.info(f"Retrieving simple store records for context: {context}")
        # Return all in this toy example
        return self.reports
