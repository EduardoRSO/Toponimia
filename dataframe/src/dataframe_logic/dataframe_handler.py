import os
import json
import pandas as pd
import re
from logging_logic.logging_handler import LoggingHandler
from tqdm import tqdm

class DataframeHandler(LoggingHandler):
    DIRECTORY_PATH = os.getcwd()
    DIRECTORY_NAME = "DataframeHandler"

    def __init__(self):
        super().__init__(self.DIRECTORY_NAME)

    @LoggingHandler.log_method("DataframeHandler", "load_json_files")
    def load_json_files(self):
        for root, _, files in os.walk(self.DIRECTORY_PATH):
            all_data = []
            json_files = [f for f in files if f.endswith('.json')]
            for file_name in tqdm(json_files, desc=f'Procurando na pasta: {root}', unit='file'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    all_data.append(data)
            if all_data:
                self._process_and_save_dataframe(all_data, root)

    def _process_and_save_dataframe(self, all_data, root):
        df = pd.DataFrame(all_data)
        self.extract_url_information(df)
        institution_name = df['institution_name'].iloc[0] if 'institution_name' in df.columns else 'unknown'
        output_csv_path = os.path.join(root, f'{institution_name}_dataframe')
        chunk_size = len(df) // 10 + 1
        for i, chunk in enumerate(range(0, len(df), chunk_size)):
            chunk_df = df.iloc[chunk:chunk + chunk_size]
            chunk_df.to_csv(f'{output_csv_path}_part_{i + 1}.csv', index=False)

    @LoggingHandler.log_method("DataframeHandler", "extract_url_information")
    def extract_url_information(self, dataframe):
        if 'url' not in dataframe.columns:
            self.log_method("DataframeHandler", "extract_url_information", False)
            raise ValueError("A coluna 'url' não está presente no DataFrame.")
        dataframe['base_url'] = dataframe['url'].apply(lambda x: x.split('/')[2] if x and isinstance(x, str) else None)
        dataframe['institution_name'] = dataframe['base_url'].apply(self._extract_institution_name)
        dataframe['subject'] = dataframe.apply(lambda row: self._extract_subject(row['url'], row['institution_name']), axis=1)

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

    @LoggingHandler.log_method("DataframeHandler", "execute", True)
    def execute(self):
        self.load_json_files()