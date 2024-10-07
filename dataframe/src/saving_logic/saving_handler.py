#1[
#1 TITULO: SAVINGHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: GERENCIAR A CRIAÇÃO DE DIRETÓRIOS E O SALVAMENTO DE INFORMAÇÕES DE REQUISIÇÕES EM ARQUIVOS JSON
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), DICIONÁRIO REQUEST_INFO (NA FUNÇÃO SAVE_REQUEST_INFO)
#1 SAIDAS: CAMINHO DO ARQUIVO JSON GERADO COM AS INFORMAÇÕES DA REQUISIÇÃO
#1 ROTINAS CHAMADAS: _CREATE_DIRECTORY, SAVE_REQUEST_INFO
#1]

import os
import json
from datetime import datetime
from logging_logic.logging_handler import LoggingHandler

class SavingHandler(LoggingHandler):
    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE SAVINGHANDLER E CRIA O DIRETÓRIO DE SALVAMENTO SE NÃO EXISTIR
    #1 ENTRADAS: NOME DO DIRETÓRIO (STRING)
    #1 DEPENDENCIAS: LOGGINGHANDLER, OS
    #1 CHAMADO POR: SAVINGHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__, _CREATE_DIRECTORY
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    @LoggingHandler.log_method('SavingHandler', '__init__')
    def __init__(self, directory_name):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI E INICIALIZA O DIRETÓRIO
        super().__init__(directory_name)
        #2 ARMAZENA O NOME DO DIRETÓRIO
        self.directory_name = directory_name
        #2 CHAMA O MÉTODO PARA CRIAR O DIRETÓRIO SE ELE NÃO EXISTIR
        self._create_directory()
    #2]

    #1[
    #1 ROTINA: _CREATE_DIRECTORY
    #1 FINALIDADE: VERIFICA SE O DIRETÓRIO EXISTE E O CRIA SE NECESSÁRIO
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: OS
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: OS.MAKEDIRS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _create_directory
    def _create_directory(self):
        #2 VERIFICA SE O DIRETÓRIO EXISTE
        if not os.path.exists(self.directory_name):
            #2 CRIA O DIRETÓRIO SE ELE NÃO EXISTIR
            os.makedirs(self.directory_name)
    #2]

    #1[
    #1 ROTINA: SAVE_REQUEST_INFO
    #1 FINALIDADE: SALVA AS INFORMAÇÕES DA REQUISIÇÃO EM UM ARQUIVO JSON DENTRO DO DIRETÓRIO ESPECIFICADO
    #1 ENTRADAS: DICIONÁRIO REQUEST_INFO (CONTENDO DADOS DA REQUISIÇÃO)
    #1 DEPENDENCIAS: JSON, OS, DATETIME
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: save_request_info
    @LoggingHandler.log_method('SavingHandler', 'save_request_info', show_output=True)
    def save_request_info(self, request_info):
        #2 GERA UM TIMESTAMP PARA O NOME DO ARQUIVO
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        #2 DEFINE O NOME DO ARQUIVO JSON COM BASE NO TIMESTAMP
        file_name = f"request_{timestamp}.json"
        #2 DEFINE O CAMINHO COMPLETO DO ARQUIVO A SER SALVO
        file_path = os.path.join(self.directory_name, file_name)
        #2 ABRE O ARQUIVO JSON EM MODO DE ESCRITA E SALVA O DICIONÁRIO REQUEST_INFO
        with open(file_path, 'w') as json_file:
            json.dump(request_info, json_file, indent=4)
        #2 RETORNA O CAMINHO DO ARQUIVO SALVO
        return file_path
    #2]
