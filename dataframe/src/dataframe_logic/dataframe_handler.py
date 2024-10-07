#1[
#1 TITULO: DATAFRAMEHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: MANIPULAR E PROCESSAR ARQUIVOS JSON, TRANSFORMANDO-OS EM DATAFRAMES E EXTRAINDO INFORMAÇÕES ÚTEIS.
#1 ENTRADAS: NENHUMA
#1 SAIDAS: ARQUIVOS CSV GERADOS A PARTIR DE DATAFRAMES
#1 ROTINAS CHAMADAS: LOAD_JSON_FILES, _PROCESS_AND_SAVE_DATAFRAME, EXTRACT_URL_INFORMATION, _EXTRACT_INSTITUTION_NAME, _EXTRACT_SUBJECT, EXECUTE
#1]

import os
import json
import pandas as pd
import re
from logging_logic.logging_handler import LoggingHandler
from tqdm import tqdm

class DataframeHandler(LoggingHandler):
    DIRECTORY_PATH = os.getcwd()
    DIRECTORY_NAME = "DataframeHandler"

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA AS VARIÁVEIS DA CLASSE DATAFRAMEHANDLER E CHAMA O CONSTRUTOR DA CLASSE PAI.
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: LOGGINGHANDLER, OS
    #1 CHAMADO POR: DATAFRAMEHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI PASSANDO O NOME DO DIRETÓRIO
        super().__init__(self.DIRECTORY_NAME)
    #2]

    #1[
    #1 ROTINA: LOAD_JSON_FILES
    #1 FINALIDADE: CARREGA TODOS OS ARQUIVOS JSON DO DIRETÓRIO E OS PROCESSA.
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: OS, JSON, TQDM, RE
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: _PROCESS_AND_SAVE_DATAFRAME
    #1]
    #2[
    #2 PSEUDOCODIGO DE: load_json_files
    @LoggingHandler.log_method("DataframeHandler", "load_json_files")
    def load_json_files(self):
        #2 ITERA SOBRE OS ARQUIVOS NO DIRETÓRIO ATUAL
        for root, _, files in os.walk(self.DIRECTORY_PATH):
            all_data = []
            #2 FILTRA ARQUIVOS COM EXTENSÃO .JSON
            json_files = [f for f in files if f.endswith('.json')]
            #2 CARREGA CADA ARQUIVO JSON E LIMPA OS DADOS
            for file_name in tqdm(json_files, desc=f'Procurando na pasta: {root}', unit='file'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    cleaned_data = {k: re.sub(r'\s+', ' ', str(v)) for k, v in data.items()}
                    all_data.append(cleaned_data)
            #2 SE EXISTIREM DADOS, PROCESSA E SALVA EM CSV
            if all_data:
                self._process_and_save_dataframe(all_data, root)
    #2]

    #1[
    #1 ROTINA: _PROCESS_AND_SAVE_DATAFRAME
    #1 FINALIDADE: PROCESSA OS DADOS E SALVA EM ARQUIVOS CSV NO DIRETÓRIO CORRESPONDENTE.
    #1 ENTRADAS: LISTA DE DICIONÁRIOS COM OS DADOS JSON E O CAMINHO DO DIRETÓRIO
    #1 DEPENDENCIAS: PANDAS, OS
    #1 CHAMADO POR: LOAD_JSON_FILES
    #1 CHAMA: EXTRACT_URL_INFORMATION
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _process_and_save_dataframe
    def _process_and_save_dataframe(self, all_data, root):
        #2 CRIA UM DATAFRAME A PARTIR DOS DADOS JSON
        df = pd.DataFrame(all_data)
        #2 EXTRAI INFORMAÇÕES DA URL E ADICIONA AO DATAFRAME
        self.extract_url_information(df)
        #2 OBTÉM O NOME DA INSTITUIÇÃO, OU DEFINE COMO 'DESCONHECIDO'
        institution_name = df['institution_name'].iloc[0] if 'institution_name' in df.columns else 'unknown'
        #2 DEFINE O CAMINHO DE SAÍDA PARA O CSV
        output_csv_path = os.path.join(root, f'{institution_name}_dataframe')
        #2 DEFINE O TAMANHO DE CADA LOTE DE CSV A SER GERADO
        chunk_size = len(df) // 10 + 1
        #2 GERA E SALVA CADA PARTE DO CSV
        for i, chunk in enumerate(range(0, len(df), chunk_size)):
            chunk_df = df.iloc[chunk:chunk + chunk_size]
            chunk_df.to_csv(f'{output_csv_path}_part_{i + 1}.csv', index=False, sep='|', quoting=1)
    #2]

    #1[
    #1 ROTINA: EXTRACT_URL_INFORMATION
    #1 FINALIDADE: EXTRAI INFORMAÇÕES RELEVANTES DAS URLS PRESENTES NO DATAFRAME.
    #1 ENTRADAS: DATAFRAME COM A COLUNA 'URL'
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: _PROCESS_AND_SAVE_DATAFRAME
    #1 CHAMA: _EXTRACT_INSTITUTION_NAME, _EXTRACT_SUBJECT
    #1]
    #2[
    #2 PSEUDOCODIGO DE: extract_url_information
    @LoggingHandler.log_method("DataframeHandler", "extract_url_information")
    def extract_url_information(self, dataframe):
        #2 VERIFICA SE A COLUNA 'URL' EXISTE NO DATAFRAME
        if 'url' not in dataframe.columns:
            raise ValueError("A coluna 'url' não está presente no DataFrame.")
        #2 EXTRAI O DOMÍNIO BASE DA URL
        dataframe['base_url'] = dataframe['url'].apply(lambda x: x.split('/')[2] if x and isinstance(x, str) else None)
        #2 EXTRAI O NOME DA INSTITUIÇÃO A PARTIR DO DOMÍNIO
        dataframe['institution_name'] = dataframe['base_url'].apply(self._extract_institution_name)
        #2 EXTRAI O ASSUNTO RELACIONADO COM A URL
        dataframe['subject'] = dataframe.apply(lambda row: self._extract_subject(row['url'], row['institution_name']), axis=1)
    #2]

    #1[
    #1 ROTINA: _EXTRACT_INSTITUTION_NAME
    #1 FINALIDADE: IDENTIFICA O NOME DA INSTITUIÇÃO BASEADO NO DOMÍNIO DA URL.
    #1 ENTRADAS: BASE_URL (STRING)
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: EXTRACT_URL_INFORMATION
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _extract_institution_name
    def _extract_institution_name(self, base_url):
        #2 VERIFICA SE O DOMÍNIO CONTÉM O TEXTO 'PREFEITURA.SP'
        if "prefeitura.sp" in base_url:
            return "Prefeitura SP"
        #2 VERIFICA SE O DOMÍNIO CONTÉM O TEXTO 'AL.SP'
        elif "al.sp" in base_url:
            return "Alesp"
        #2 VERIFICA SE O DOMÍNIO CONTÉM O TEXTO 'LEISMUNICIPAIS.COM.BR'
        elif "leismunicipais.com.br" in base_url:
            return "Camara SP"
        #2 RETORNA 'OUTROS' SE NENHUMA CONDIÇÃO FOR ATENDIDA
        else:
            return "Outros"
    #2]

    #1[
    #1 ROTINA: _EXTRACT_SUBJECT
    #1 FINALIDADE: EXTRAI O ASSUNTO DA URL COM BASE NO NOME DA INSTITUIÇÃO.
    #1 ENTRADAS: URL (STRING), NOME DA INSTITUIÇÃO (STRING)
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: EXTRACT_URL_INFORMATION
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _extract_subject
    def _extract_subject(self, url, institution_name):
        #2 EXTRAI O ASSUNTO PARA INSTITUIÇÕES DA ALESP
        if institution_name == "Alesp":
            match = re.search(r'palavraChaveDecode=([^&]+)&?', url)
            return match.group(1) if match else ""
        #2 EXTRAI O ASSUNTO PARA INSTITUIÇÕES DA PREFEITURA SP
        elif institution_name == "Prefeitura SP":
            match = re.search(r'assunto=([^&]+)', url)
            return match.group(1) if match else ""
        #2 EXTRAI O ASSUNTO PARA INSTITUIÇÕES DA CÂMARA SP
        elif institution_name == "Camara SP":
            match = re.search(r'q=([^&]+)&?', url)
            return match.group(1) if match else ""
        #2 RETORNA STRING VAZIA SE NÃO HOUVER MATCH
        return ""
    #2]

    #1[
    #1 ROTINA: EXECUTE
    #1 FINALIDADE: EXECUTA A ROTINA PRINCIPAL DE CARREGAMENTO E PROCESSAMENTO DOS ARQUIVOS JSON.
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: LOGGINGHANDLER
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: LOAD_JSON_FILES
    #1]
    #2[
    #2 PSEUDOCODIGO DE: execute
    @LoggingHandler.log_method("DataframeHandler", "execute", True)
    def execute(self):
        #2 INICIA O PROCESSO DE CARREGAMENTO E PROCESSAMENTO DOS ARQUIVOS JSON
        self.load_json_files()
    #2]
