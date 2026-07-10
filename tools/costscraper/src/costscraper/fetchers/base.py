"""Fetcher base class."""

from abc import ABC, abstractmethod


class Fetcher(ABC):
    """Abstract base class for provider price fetchers."""

    @abstractmethod
    def fetchPrices(self):
        """Return a dict mapping normalized model identifier to price data.

        Price data format:
            {"input": float | None, "output": float | None}
        """
        pass
