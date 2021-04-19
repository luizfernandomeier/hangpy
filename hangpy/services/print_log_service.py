from hangpy.services import LogService


class PrintLogService(LogService):
    """
    Logger that prints the messages on the console.
    """

    def log(self, message: str):
        print(message)
