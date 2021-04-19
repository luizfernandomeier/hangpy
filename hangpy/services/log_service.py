from abc import ABC, abstractmethod


class LogService(ABC):
    """
    Provides an interface to add a logger to HangPy.
    """

    @abstractmethod
    def log(self, message: str):
        """
        Sends a message to the logger implementation.

        Args:
            message (str)
        """

        pass
