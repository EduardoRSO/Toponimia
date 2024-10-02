from logging_logic.logging_handler import LoggingHandler
from requesting_logic.requesting_handler import RequestingHandler
from saving_logic.saving_handler import SavingHandler
from text_logic.text_handler import TextHandler
from toponym_logic.toponym_handler import ToponymHandler

class ScrapingHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.requesting_handler = RequestingHandler(directory_name)
        self.saving_handler = SavingHandler(directory_name)
        self.text_handler = TextHandler(directory_name)
        self.toponym_handler = ToponymHandler(directory_name)

    @LoggingHandler.log_method("ScrapingHandler", "process_response")
    def process_response(self, data_dict):
        """
        Processa o dicionário inserindo os campos 'extracted_text', 'lemmatized_text' e 'extracted_toponyms'.
        Após inserir os novos campos, o dicionário será salvo usando self.saving_handler.save_request_info.
        
        - extracted_text: texto bruto extraído do 'response_string'.
        - lemmatized_text: texto lematizado.
        - extracted_toponyms: lista de topônimos extraídos.
        """
        extracted_text = self.text_handler.extract_raw_text(data_dict['response_string'])
        data_dict['extracted_text'] = extracted_text
        lemmatized_text, extracted_toponyms = self.toponym_handler.lemmatize_and_extract_toponyms(extracted_text)
        data_dict['lemmatized_text'] = lemmatized_text
        data_dict['extracted_toponyms'] = extracted_toponyms
        self.saving_handler.save_request_info(data_dict)