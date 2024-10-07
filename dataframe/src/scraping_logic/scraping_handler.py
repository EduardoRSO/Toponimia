#1[
#1 TITULO: SCRAPINGHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZAR O PROCESSO DE SCRAPING, EXTRAÇÃO DE TEXTO, LEMATIZAÇÃO E SALVAMENTO DOS DADOS EM ARQUIVOS JSON
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), DICIONÁRIO DATA_DICT (NA FUNÇÃO PROCESS_RESPONSE)
#1 SAIDAS: DICIONÁRIO PROCESSADO COM CAMPOS EXTRAÍDOS E ARQUIVO JSON COM AS INFORMAÇÕES SALVAS
#1 ROTINAS CHAMADAS: PROCESS_RESPONSE, SAVE_REQUEST_INFO (SAVINGHANDLER), EXTRACT_RAW_TEXT (TEXTHANDLER), LEMMATIZE_AND_EXTRACT_TOPONYMS (TOPONYMHANDLER)
#1]

from logging_logic.logging_handler import LoggingHandler
from requesting_logic.requesting_handler import RequestingHandler
from saving_logic.saving_handler import SavingHandler
from text_logic.text_handler import TextHandler
from toponym_logic.toponym_handler import ToponymHandler

class ScrapingHandler(LoggingHandler):
    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE SCRAPINGHANDLER E CONFIGURA AS DEPENDÊNCIAS NECESSÁRIAS
    #1 ENTRADAS: NOME DO DIRETÓRIO (STRING)
    #1 DEPENDENCIAS: REQUESTINGHANDLER, SAVINGHANDLER, TEXTHANDLER, TOPONYMHANDLER, LOGGINGHANDLER
    #1 CHAMADO POR: SCRAPINGHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__, REQUESTINGHANDLER, SAVINGHANDLER, TEXTHANDLER, TOPONYMHANDLER
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, directory_name):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI E INICIALIZA O DIRETÓRIO
        super().__init__(directory_name)
        #2 INICIALIZA O HANDLER DE REQUISIÇÕES
        self.requesting_handler = RequestingHandler(directory_name)
        #2 INICIALIZA O HANDLER DE SALVAMENTO
        self.saving_handler = SavingHandler(directory_name)
        #2 INICIALIZA O HANDLER DE TEXTO
        self.text_handler = TextHandler(directory_name)
        #2 INICIALIZA O HANDLER DE TOPÔNIMOS
        self.toponym_handler = ToponymHandler(directory_name)
    #2]

    #1[
    #1 ROTINA: PROCESS_RESPONSE
    #1 FINALIDADE: PROCESSA O DICIONÁRIO DE RESPOSTA, EXTRAINDO TEXTO BRUTO, LEMATIZANDO E EXTRAINDO TOPÔNIMOS, E SALVA AS INFORMAÇÕES
    #1 ENTRADAS: DICIONÁRIO DATA_DICT (COM CAMPOS COMO RESPONSE_STRING)
    #1 DEPENDENCIAS: TEXTHANDLER, TOPONYMHANDLER, SAVINGHANDLER
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: EXTRACT_RAW_TEXT (TEXTHANDLER), LEMMATIZE_AND_EXTRACT_TOPONYMS (TOPONYMHANDLER), SAVE_REQUEST_INFO (SAVINGHANDLER)
    #1]
    #2[
    #2 PSEUDOCODIGO DE: process_response
    @LoggingHandler.log_method("ScrapingHandler", "process_response")
    def process_response(self, data_dict):
        #2 EXTRAI O TEXTO BRUTO A PARTIR DA RESPOSTA
        extracted_text = self.text_handler.extract_raw_text(data_dict['response_string'])
        #2 ADICIONA O TEXTO EXTRAÍDO AO DICIONÁRIO
        data_dict['extracted_text'] = extracted_text
        #2 LEMATIZA O TEXTO E EXTRAI OS TOPÔNIMOS
        lemmatized_text, extracted_toponyms = self.toponym_handler.lemmatize_and_extract_toponyms(extracted_text)
        #2 ADICIONA O TEXTO LEMATIZADO E OS TOPÔNIMOS AO DICIONÁRIO
        data_dict['lemmatized_text'] = lemmatized_text
        data_dict['extracted_toponyms'] = extracted_toponyms
        #2 SALVA O DICIONÁRIO PROCESSADO USANDO O SAVINGHANDLER
        self.saving_handler.save_request_info(data_dict)
    #2]
