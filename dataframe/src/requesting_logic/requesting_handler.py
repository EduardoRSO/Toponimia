#1[
#1 TITULO: REQUESTINGHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZAR REQUISIÇÕES HTTP (GET E POST) E LOGAR O TEMPO DE RESPOSTA E OUTRAS INFORMAÇÕES RELEVANTES
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), MÉTODO HTTP, URL, KWARGS (DADOS ADICIONAIS OPCIONAIS)
#1 SAIDAS: DICIONÁRIO CONTENDO DADOS DA REQUISIÇÃO E RESPOSTA, INCLUINDO TEMPO, TAMANHO E ERROS (SE HOUVER)
#1 ROTINAS CHAMADAS: SET_METHOD_MAPPING, _REQUEST_WRAPPER, MAKE_REQUEST
#1]

import requests
import time
from datetime import datetime
from logging_logic.logging_handler import LoggingHandler

class RequestingHandler(LoggingHandler):
    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE REQUESTINGHANDLER E CONFIGURA O MAPEAMENTO DE MÉTODOS HTTP
    #1 ENTRADAS: NOME DO DIRETÓRIO (STRING)
    #1 DEPENDENCIAS: LOGGINGHANDLER
    #1 CHAMADO POR: REQUESTINGHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__, SET_METHOD_MAPPING
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, directory_name):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI PASSANDO O NOME DO DIRETÓRIO
        super().__init__(directory_name)
        #2 CONFIGURA O MAPEAMENTO DE MÉTODOS HTTP
        self.set_method_mapping()
    #2]

    #1[
    #1 ROTINA: SET_METHOD_MAPPING
    #1 FINALIDADE: DEFINE O MAPEAMENTO DOS MÉTODOS HTTP (GET E POST)
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: REQUESTS
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_method_mapping
    @LoggingHandler.log_method('RequestingHandler', 'set_method_mapping', show_output=False, show_parameters=True)
    def set_method_mapping(self):
        #2 DEFINE O MAPEAMENTO DE MÉTODOS HTTP 'GET' E 'POST'
        self.method_mapping = {
            'GET': requests.get,
            'POST': requests.post
        }
    #2]

    #1[
    #1 ROTINA: _REQUEST_WRAPPER
    #1 FINALIDADE: ENVOLVE A EXECUÇÃO DA REQUISIÇÃO HTTP E COLETA DADOS COMO TEMPO DE RESPOSTA E TAMANHO DA RESPOSTA
    #1 ENTRADAS: FUNÇÃO DO MÉTODO HTTP, URL, DICIONÁRIO REQUEST_INFO, KWARGS OPCIONAIS
    #1 DEPENDENCIAS: TIME, REQUESTS
    #1 CHAMADO POR: MAKE_REQUEST
    #1 CHAMA: MÉTODOS HTTP (GET OU POST), RAISE_FOR_STATUS (REQUESTS)
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _request_wrapper
    def _request_wrapper(self, method_function, url, request_info, **kwargs):
        try:
            #2 OBTÉM O TEMPO DE INÍCIO DA REQUISIÇÃO
            start_time = time.time()
            #2 EXECUTA O MÉTODO HTTP COM A URL E OS KWARGS
            response = method_function(url, **kwargs)
            #2 OBTÉM O TEMPO FINAL DA REQUISIÇÃO
            end_time = time.time()
            #2 CALCULA O TEMPO DE RESPOSTA
            request_info["response_time"] = end_time - start_time
            #2 OBTÉM O TAMANHO DO CONTEÚDO DA RESPOSTA
            request_info["response_length"] = len(response.content)
            #2 SALVA O TEXTO DA RESPOSTA
            request_info["response_string"] = response.text
            #2 VERIFICA SE HOUVE ALGUM ERRO NA REQUISIÇÃO
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            #2 EM CASO DE ERRO, ARMAZENA A MENSAGEM DE ERRO NO DICIONÁRIO
            request_info["error"] = str(e)
        #2 RETORNA AS INFORMAÇÕES DA REQUISIÇÃO
        return request_info
    #2]

    #1[
    #1 ROTINA: MAKE_REQUEST
    #1 FINALIDADE: FAZ A REQUISIÇÃO HTTP USANDO O MÉTODO ESPECIFICADO (GET OU POST) E RETORNA AS INFORMAÇÕES DA REQUISIÇÃO
    #1 ENTRADAS: MÉTODO (GET OU POST), URL, KWARGS OPCIONAIS
    #1 DEPENDENCIAS: DATETIME, REQUESTS, TIME
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: _REQUEST_WRAPPER
    #1]
    #2[
    #2 PSEUDOCODIGO DE: make_request
    @LoggingHandler.log_method('RequestingHandler', 'make_request', show_output=False, show_parameters=True)
    def make_request(self, method, url, **kwargs):
        #2 VERIFICA SE O MÉTODO É SUPORTADO (GET OU POST)
        if method.upper() not in self.method_mapping:
            raise ValueError(f"Method {method} not supported. Use 'GET' or 'POST'.")
        #2 CRIA UM DICIONÁRIO PARA ARMAZENAR AS INFORMAÇÕES DA REQUISIÇÃO
        request_info = {
            "url": url,
            "method": method.upper(),
            "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "response_time": "",
            "response_length": "",
            "response_string": "",
            "error": ""
        }
        #2 CHAMA O MÉTODO _REQUEST_WRAPPER PARA REALIZAR A REQUISIÇÃO E RETORNAR AS INFORMAÇÕES
        return self._request_wrapper(self.method_mapping[method.upper()], url, request_info, **kwargs)
    #2]
