from bs4 import BeautifulSoup
from logging_logic.logging_handler import LoggingHandler

class TextHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.directory_name = directory_name

    @LoggingHandler.log_method("TextHandler", "extract_raw_text")    
    def extract_raw_text(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            raw_text = soup.get_text(separator=' ', strip=True)
            return raw_text
        except Exception as e:
            return ""
