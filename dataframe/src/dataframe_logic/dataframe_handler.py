import os
import json
import pandas as pd
import re
from logging_logic.logging_handler import LoggingHandler

class DataframeHandler(LoggingHandler):
    DIRECTORY_PATH = ''
    OUTPUT_PATH = 'dataframe.csv'

    def __init__(self):
        super().__init__()
        self.dataframe = pd.DataFrame()

    @LoggingHandler.log_method("DataframeHandler", "load_json_files")
    def load_json_files(self):
        all_data = []
        for file_name in os.listdir(self.DIRECTORY_PATH):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.DIRECTORY_PATH, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    all_data.append(data)
        self.dataframe = pd.DataFrame(all_data)

    @LoggingHandler.log_method("DataframeHandler", "extract_url_information")
    def extract_url_information(self):
        if 'url' not in self.dataframe.columns:
            self.log_method("DataframeHandler", "extract_url_information", False)
            raise ValueError("A coluna 'url' não está presente no DataFrame.")
        self.dataframe['base_url'] = self.dataframe['url'].apply(lambda x: x.split('/')[2] if x and isinstance(x, str) else None)
        self.dataframe['institution_name'] = self.dataframe['base_url'].apply(self._extract_institution_name)
        self.dataframe['subject'] = self.dataframe.apply(lambda row: self._extract_subject(row['url'], row['institution_name']), axis=1)

    def _extract_institution_name(self, base_url):
        if "prefeitura.sp" in base_url:
            return "Prefeitura SP"
        elif "al.sp" in base_url:
            return "Alesp"
        elif "leismunicipais.com.br" in base_url:
            return "Camara SP"
        else:
            return "Outros"

    def _extract_subject(self, url, institution_name):
        if institution_name == "Alesp":
            match = re.search(r'palavraChaveDecode=([^&]+)&?', url)
            return match.group(1) if match else ""
        elif institution_name == "Prefeitura SP":
            match = re.search(r'assunto=([^&]+)', url)
            return match.group(1) if match else ""
        elif institution_name == "Camara SP":
            match = re.search(r'q=([^&]+)&?', url)
            return match.group(1) if match else ""
        return ""

    @LoggingHandler.log_method("DataframeHandler", "save_dataframe", True)
    def save_dataframe(self):
        self.dataframe.to_csv(self.OUTPUT_PATH, index=False)

    @LoggingHandler.log_method("DataframeHandler", "execute", True)
    def execute(self):
        self.load_json_files()
        self.extract_url_information()
        self.save_dataframe()

if __name__ == '__main__':
    df_handler = DataframeHandler()
    df_handler.execute()
