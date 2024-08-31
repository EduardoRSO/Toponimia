import os
import json
from datetime import datetime
from logging_logic.logging_handler import LoggingHandler

class SavingHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.directory_name = directory_name
        self._create_directory()

    @LoggingHandler.log_method('SavingHandler', '__init__', show_output=False, show_parameters=True)
    def _create_directory(self):
        if not os.path.exists(self.directory_name):
            os.makedirs(self.directory_name)

    @LoggingHandler.log_method('SavingHandler', 'save_request_info', show_output=True)
    def save_request_info(self, request_info):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        file_name = f"request_{timestamp}.json"
        file_path = os.path.join(self.directory_name, file_name)
        with open(file_path, 'w') as json_file:
            json.dump(request_info, json_file, indent=4)
        return file_path
