import re
from bs4 import BeautifulSoup
from logging_logic.logging_handler import LoggingHandler

class TextHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.directory_name = directory_name

    @LoggingHandler.log_method("TextHandler", "extract_raw_text")
    def extract_raw_text(self, html_content):
        try:
            # Extrair texto bruto com BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            raw_text = soup.get_text(separator=' ', strip=True)

            # Remover caracteres não pertencentes ao alfabeto português
            clean_text = self._filter_portuguese_text(raw_text)

            return clean_text
        except Exception as e:
            self.log_method("TextHandler", "extract_raw_text", False)
            return ""

    def _filter_portuguese_text(self, text):
        """
        Remove caracteres que não fazem parte do alfabeto português,
        números e sinais de pontuação básicos.
        """
        # Expressão regular para manter apenas caracteres válidos do português
        portuguese_pattern = re.compile(r"[^a-zA-ZÀ-ÿ0-9.,!?;:\-\(\)\[\]\s]")
        
        # Substitui os caracteres não permitidos por uma string vazia
        filtered_text = portuguese_pattern.sub('', text)

        return filtered_text
