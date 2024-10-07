#1[
#1 TITULO: LOGGING HANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: GERENCIA O LOGGING PARA UMA CLASSE, PERMITINDO A CRIACAO DE LOGS E FORMATO ESPECIFICO, E LOGAR EXECUCAO DE METODOS COM PARAMETROS E RESULTADOS
#1 ENTRADAS: NOME DO DIRETORIO PARA ARMAZENAR OS LOGS, NOME DA CLASSE, NOME DO METODO, OPCOES PARA LOGAR PARAMETROS E RESULTADOS
#1 SAIDAS: LOGS EM ARQUIVO DE TEXTO
#1 ROTINAS CHAMADAS: __INIT__, LOG_METHOD
#1 DEPENDENCIAS: LOGGING, OS
#1]

import logging
import os

#1[
#1 ROTINA: __INIT__
#1 FINALIDADE: INICIALIZA O MANIPULADOR DE LOGS E CONFIGURA O FORMATO DE LOGS PARA A CLASSE LOGGINGHANDLER
#1 ENTRADAS: NOME DO DIRETORIO PARA ARMAZENAR OS LOGS
#1 DEPENDENCIAS: LOGGING, OS
#1 CHAMADO POR: LOGGINGHANDLER
#1 CHAMA: OS.MAKEDIRS (SE O DIRETORIO NAO EXISTIR), LOGGING.GETLOGGER, LOGGING.FILEHANDLER, LOGGING.FORMATTER
#1]
#2[
#2 PSEUDOCODIGO DE: __INIT__
class LoggingHandler:
    def __init__(self, directory_name):
        #2 OBTEM UM LOGGER ASSOCIADO AO NOME DA CLASSE
        self.logger = logging.getLogger(self.__class__.__name__)
        #2 VERIFICA SE O DIRETORIO EXISTE, SE NAO, CRIA O DIRETORIO
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        #2 DEFINE O CAMINHO DO ARQUIVO DE LOGS COMO LOGS.TXT
        file_path = os.path.join(directory_name, "logs.txt")
        #2 CRIA UM MANIPULADOR DE LOG PARA O ARQUIVO
        handler = logging.FileHandler(file_path)
        #2 DEFINE O FORMATO DO LOG COM O NOME DA CLASSE E O NOME DO METODO
        formatter = logging.Formatter("[+] %(class_name)s.%(method_name)s %(message)s")
        handler.setFormatter(formatter)
        #2 ADICIONA O MANIPULADOR AO LOGGER
        self.logger.addHandler(handler)
        #2 DEFINE O NIVEL DE LOG PARA INFO
        self.logger.setLevel(logging.INFO)
#2]

#1[
#1 ROTINA: LOG_METHOD
#1 FINALIDADE: DECORADOR PARA LOGAR A EXECUCAO DE METODOS, COM OPCOES PARA EXIBIR PARAMETROS E RESULTADOS
#1 ENTRADAS: NOME DA CLASSE, NOME DO METODO, OPCOES DE EXIBIR PARAMETROS E EXIBIR RESULTADO
#1 DEPENDENCIAS: LOGGING
#1 CHAMADO POR: LOGGINGHANDLER
#1 CHAMA: FUNC (METODO DECORADO)
#1]
#2[
#2 PSEUDOCODIGO DE: LOG_METHOD
    @staticmethod
    def log_method(class_name, method_name, show_output=False, show_parameters=False):
        #2 DEFINE UM DECORADOR PARA O METODO
        def decorator(func):
            #2 CRIA O WRAPPER QUE ENVOLVE O METODO ORIGINAL
            def wrapper(self, *args, **kwargs):
                #2 SE EXIBIR PARAMETROS, GERA UMA STRING COM OS PARAMETROS
                if show_parameters:
                    parameters = f"Parameters: args={args}, kwargs={kwargs}"
                else:
                    parameters = ""
                #2 LOGA OS PARAMETROS UTILIZANDO O LOGGER
                logging.getLogger(class_name).info(parameters, extra={'class_name': class_name, 'method_name': method_name})
                #2 EXECUTA O METODO ORIGINAL E OBTEM O RESULTADO
                result = func(self, *args, **kwargs)
                #2 SE EXIBIR O RESULTADO, GERA UMA MENSAGEM DE LOG COM O RESULTADO
                if show_output:
                    output_message = f"Output: {result}"
                    logging.getLogger(class_name).info(output_message, extra={'class_name': class_name, 'method_name': method_name})
                #2 RETORNA O RESULTADO DA EXECUCAO DO METODO ORIGINAL
                return result
            #2 RETORNA O WRAPPER COMO O NOVO METODO DECORADO
            return wrapper
        #2 RETORNA O DECORADOR
        return decorator
#2]
