from logging_logic.logging_handler import LoggingHandler
from requesting_logic.requesting_handler import RequestingHandler
from saving_logic.saving_handler import SavingHandler

class ScrapingHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.requesting_handler = RequestingHandler(directory_name)
        self.saving_handler = SavingHandler(directory_name)