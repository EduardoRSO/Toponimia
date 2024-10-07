#1[
#1 TITULO: TEXTHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZAR EXTRAÇÃO E FILTRAGEM DE TEXTO BRUTO A PARTIR DE CONTEÚDO HTML
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), CONTEÚDO HTML (NA FUNÇÃO EXTRACT_RAW_TEXT)
#1 SAIDAS: TEXTO LIMPO EM MINÚSCULAS EXTRAÍDO DO CONTEÚDO HTML
#1 ROTINAS CHAMADAS: EXTRACT_RAW_TEXT, _FILTER_PORTUGUESE_TEXT
#1]

import re
from bs4 import BeautifulSoup
from logging_logic.logging_handler import LoggingHandler

class TextHandler(LoggingHandler):
    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE TEXTHANDLER E CONFIGURA O DIRETÓRIO
    #1 ENTRADAS: NOME DO DIRETÓRIO (STRING)
    #1 DEPENDENCIAS: LOGGINGHANDLER
    #1 CHAMADO POR: TEXTHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, directory_name):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI E INICIALIZA O DIRETÓRIO
        super().__init__(directory_name)
        #2 ARMAZENA O NOME DO DIRETÓRIO
        self.directory_name = directory_name
    #2]

    #1[
    #1 ROTINA: EXTRACT_RAW_TEXT
    #1 FINALIDADE: EXTRAI O TEXTO BRUTO DO CONTEÚDO HTML E O FILTRA PARA REMOVER CARACTERES INDESEJADOS
    #1 ENTRADAS: CONTEÚDO HTML (STRING)
    #1 DEPENDENCIAS: BEAUTIFULSOUP, RE
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: _FILTER_PORTUGUESE_TEXT
    #1]
    #2[
    #2 PSEUDOCODIGO DE: extract_raw_text
    def extract_raw_text(self, html_content):
        try:
            #2 ANALISA O CONTEÚDO HTML USANDO BEAUTIFULSOUP
            soup = BeautifulSoup(html_content, 'html.parser')
            #2 EXTRAI O TEXTO BRUTO DO CONTEÚDO HTML
            raw_text = soup.get_text(separator=' ', strip=True)
            #2 FILTRA O TEXTO PARA REMOVER CARACTERES NÃO PERTENCENTES AO PORTUGUÊS
            clean_text = self._filter_portuguese_text(raw_text)
            #2 RETORNA O TEXTO FILTRADO EM MINÚSCULAS
            return clean_text.lower()
        except Exception as e:
            #2 RETORNA UMA STRING VAZIA EM CASO DE FALHA
            return ""
    #2]

    #1[
    #1 ROTINA: _FILTER_PORTUGUESE_TEXT
    #1 FINALIDADE: FILTRA O TEXTO PARA REMOVER CARACTERES QUE NÃO SÃO DO PORTUGUÊS
    #1 ENTRADAS: TEXTO BRUTO (STRING)
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: EXTRACT_RAW_TEXT
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _filter_portuguese_text
    def _filter_portuguese_text(self, text):
        #2 DEFINE UM PADRÃO PARA MANTER APENAS CARACTERES PORTUGUESES, NÚMEROS E PONTUAÇÃO
        portuguese_pattern = re.compile(r"[^a-zA-ZÀ-ÿ0-9.,!?;:\-\(\)\[\]\s]")
        #2 APLICA O PADRÃO PARA REMOVER CARACTERES INDESEJADOS
        filtered_text = portuguese_pattern.sub('', text)
        #2 RETORNA O TEXTO FILTRADO
        return filtered_text
    #2]
