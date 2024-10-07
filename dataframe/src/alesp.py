#1[
#1 TITULO: ALESP SCRAPPER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZAR O SCRAPING DE NORMAS DA ASSEMBLEIA LEGISLATIVA DO ESTADO DE SÃO PAULO (ALESP) COM BASE EM DETERMINADOS ASSUNTOS
#1 ENTRADAS: NOME DO DIRETÓRIO, ASSUNTO (NA FUNÇÃO SCRAPE)
#1 SAIDAS: DADOS DE RESPOSTA PROCESSADOS, URLS VISITADAS
#1 ROTINAS CHAMADAS: SCRAPE, BUILD_URL, PARSE_CONTENT, EXTRACT_LINKS, SCRAPE_LINKS, SCRAPE_ALL_SUBJECTS
#1]

import time
import urllib.parse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from logging_logic.logging_handler import LoggingHandler
from scraping_logic.scraping_handler import ScrapingHandler

class AlespScrapper(ScrapingHandler):
    BASE_URL = "https://www.al.sp.gov.br/norma"
    NORMA_BASE_URL = "https://www.al.sp.gov.br"
    SUBJECTS = ["Alteração", "Mudança", "Modificação", "Reforma", "Transformação", "Troca", "Reajuste", "Revisão", "Ajuste", "Correção"]
    DIRECTORY_NAME = "Alesp"
    SLEEP = 15
    MAX_ERROR = 3

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE ALESP SCRAPPER E CONFIGURA AS VARIÁVEIS INICIAIS E O DIRETÓRIO DE SALVAMENTO
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: LOGGINGHANDLER, SCRAPINGHANDLER
    #1 CHAMADO POR: ALESP SCRAPPER
    #1 CHAMA: SCRAPINGHANDLER.__INIT__
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __INIT__
    @LoggingHandler.log_method('AlespScrapper', '__init__', show_parameters=False, show_output=False)
    def __init__(self):
        #2 INICIALIZA A CLASSE PAI E O DIRETÓRIO
        super().__init__(self.DIRECTORY_NAME)
        #2 INICIALIZA O CONJUNTO DE URLS VISITADAS
        self.visited_urls = set()
    #2]

    #1[
    #1 ROTINA: SCRAPE
    #1 FINALIDADE: REALIZAR O SCRAPING DE NORMAS COM BASE NO ASSUNTO ESPECIFICADO
    #1 ENTRADAS: ASSUNTO (STRING)
    #1 DEPENDENCIAS: URLLIB, TIME, REQUESTINGHANDLER
    #1 CHAMADO POR: USUÁRIO, SCRAPE_ALL_SUBJECTS
    #1 CHAMA: BUILD_URL, MAKE_REQUEST (REQUESTINGHANDLER), PROCESS_RESPONSE, PARSE_CONTENT, EXTRACT_LINKS, SCRAPE_LINKS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: SCRAPE
    @LoggingHandler.log_method('AlespScrapper', 'scrape', show_parameters=False, show_output=False)
    def scrape(self, subject):
        #2 ESCAPA O ASSUNTO PARA FORMATO DE URL E DEPOIS DECODIFICA
        escaped_subject = urllib.parse.quote(subject)
        decoded_subject = urllib.parse.unquote(escaped_subject)
        page_number = 1
        error_count = 0
        #2 REALIZA O LOOP PARA TENTAR ACESSAR PÁGINAS ENQUANTO O NÚMERO MÁXIMO DE ERROS NÃO FOR ALCANÇADO
        while error_count < self.MAX_ERROR:
            #2 CONSTROI A URL COM BASE NO ASSUNTO E NÚMERO DA PÁGINA
            url = self.build_url(page_number, escaped_subject, decoded_subject)
            #2 REALIZA A REQUISIÇÃO HTTP
            content = self.requesting_handler.make_request('GET', url)
            #2 PROCESSA A RESPOSTA
            self.process_response(content)
            if not content.get('error'):
                #2 ANALISA O CONTEÚDO HTML
                parsed_content = self.parse_content(content['response_string'])
                #2 EXTRAI OS LINKS ENCONTRADOS NO CONTEÚDO HTML
                links = self.extract_links(parsed_content)
                #2 REALIZA O SCRAPING DOS LINKS ENCONTRADOS
                self.scrape_links(links)
                error_count = 0
            else:
                error_count += 1
            page_number += 1
            time.sleep(self.SLEEP)
    #2]

    #1[
    #1 ROTINA: BUILD_URL
    #1 FINALIDADE: CONSTRUIR A URL PARA REALIZAR A REQUISIÇÃO HTTP BASEADO NO ASSUNTO E NO NÚMERO DA PÁGINA
    #1 ENTRADAS: NÚMERO DA PÁGINA (INT), ASSUNTO ESCAPADO (STRING), ASSUNTO DECODIFICADO (STRING)
    #1 DEPENDENCIAS: NENHUMA
    #1 CHAMADO POR: SCRAPE
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: BUILD_URL
    @LoggingHandler.log_method('AlespScrapper', 'build_url', show_parameters=False, show_output=False)
    def build_url(self, page_number, escaped_subject, decoded_subject):
        #2 CONSTROI A URL PARA BUSCA DE NORMAS COM BASE NO NÚMERO DA PÁGINA E NO ASSUNTO
        return (f"{self.BASE_URL}/resultados?page={page_number}&size=10&tipoPesquisa=E&"
                f"buscaLivreEscape=&buscaLivreDecode=&_idsTipoNorma=1&idsTipoNorma=9&"
                f"idsTipoNorma=2&idsTipoNorma=55&idsTipoNorma=3&idsTipoNorma=28&"
                f"idsTipoNorma=25&idsTipoNorma=1&idsTipoNorma=19&idsTipoNorma=14&"
                f"idsTipoNorma=12&idsTipoNorma=21&idsTipoNorma=22&idsTipoNorma=23&"
                f"idsTipoNorma=59&nuNorma=&ano=&complemento=&dtNormaInicio=&dtNormaFim=&"
                f"idTipoSituacao=0&_idsTema=1&palavraChaveEscape={escaped_subject}&"
                f"palavraChaveDecode={decoded_subject}&_idsAutorPropositura=1&_temQuestionamentos=on")
    #2]

    #1[
    #1 ROTINA: PARSE_CONTENT
    #1 FINALIDADE: ANALISAR O CONTEÚDO HTML OBTIDO NA REQUISIÇÃO E TRANSFORMÁ-LO EM UM OBJETO BEAUTIFULSOUP
    #1 ENTRADAS: CONTEÚDO HTML (STRING)
    #1 DEPENDENCIAS: BEAUTIFULSOUP
    #1 CHAMADO POR: SCRAPE
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: PARSE_CONTENT
    @LoggingHandler.log_method('AlespScrapper', 'parse_content', show_parameters=False, show_output=False)
    def parse_content(self, content):
        #2 TRANSFORMA O CONTEÚDO HTML EM UM OBJETO BEAUTIFULSOUP PARA FACILITAR A EXTRAÇÃO DE DADOS
        return BeautifulSoup(content, 'html.parser')
    #2]

    #1[
    #1 ROTINA: EXTRACT_LINKS
    #1 FINALIDADE: EXTRAIR LINKS RELEVANTES DO CONTEÚDO HTML ANALISADO
    #1 ENTRADAS: CONTEÚDO HTML ANALISADO (OBJETO BEAUTIFULSOUP)
    #1 DEPENDENCIAS: BEAUTIFULSOUP
    #1 CHAMADO POR: SCRAPE
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: EXTRACT_LINKS
    @LoggingHandler.log_method('AlespScrapper', 'extract_links', show_parameters=False, show_output=False)
    def extract_links(self, parsed_content):
        #2 EXTRAI TODOS OS LINKS QUE CONTÊM 'NORMA' NO CAMINHO DO HREF
        return [a['href'] for a in parsed_content.find_all('a', href=True) if 'norma' in a['href']]
    #2]

    #1[
    #1 ROTINA: SCRAPE_LINKS
    #1 FINALIDADE: REALIZAR O SCRAPING DE CADA LINK EXTRAÍDO, SEGUINDO OS LINKS E PROCESSANDO AS RESPOSTAS
    #1 ENTRADAS: LISTA DE LINKS (LISTA DE STRINGS)
    #1 DEPENDENCIAS: TIME, REQUESTINGHANDLER
    #1 CHAMADO POR: SCRAPE
    #1 CHAMA: MAKE_REQUEST (REQUESTINGHANDLER), PROCESS_RESPONSE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: SCRAPE_LINKS
    @LoggingHandler.log_method('AlespScrapper', 'scrape_links', show_parameters=False, show_output=False)
    def scrape_links(self, links):
        #2 ITERA SOBRE CADA LINK EXTRAÍDO
        for link in links:
            #2 CRIA A URL COMPLETA CONCATENANDO O LINK COM A BASE_URL DA NORMA
            full_url = f"{self.NORMA_BASE_URL}{link}"
            #2 VERIFICA SE A URL JÁ FOI VISITADA
            if full_url not in self.visited_urls:
                #2 ADICIONA A URL AO CONJUNTO DE URLs VISITADAS
                self.visited_urls.add(full_url)
                #2 FAZ A REQUISIÇÃO PARA A URL DO LINK
                content = self.requesting_handler.make_request('GET', full_url)
                #2 PROCESSA A RESPOSTA RECEBIDA
                self.process_response(content)
                #2 AGUARDA O TEMPO CONFIGURADO ENTRE REQUISIÇÕES
                time.sleep(self.SLEEP)
    #2]

    #1[
    #1 ROTINA: SCRAPE_ALL_SUBJECTS
    #1 FINALIDADE: REALIZAR O SCRAPING DE TODOS OS ASSUNTOS DEFINIDOS NA VARIÁVEL SUBJECTS UTILIZANDO MÚLTIPLAS THREADS
    #1 ENTRADAS: NENHUMA (UTILIZA OS ASSUNTOS DA VARIÁVEL DE CLASSE SUBJECTS)
    #1 DEPENDENCIAS: THREADPOOLEXECUTOR
    #1 CHAMADO POR: USUÁRIO, FUNÇÃO MAIN
    #1 CHAMA: SCRAPE (PARA CADA ASSUNTO)
    #1]
    #2[
    #2 PSEUDOCODIGO DE: SCRAPE_ALL_SUBJECTS
    @LoggingHandler.log_method('AlespScrapper', 'scrape_all_subjects', show_parameters=False, show_output=False)
    def scrape_all_subjects(self):
        #2 UTILIZA UM THREADPOOLEXECUTOR PARA PARALELIZAR O PROCESSO DE SCRAPING PARA TODOS OS ASSUNTOS
        with ThreadPoolExecutor(max_workers=len(self.SUBJECTS)) as executor:
            #2 EXECUTA A FUNÇÃO SCRAPE PARA CADA ASSUNTO EM SUBJECTS SIMULTANEAMENTE
            executor.map(self.scrape, self.SUBJECTS)
    #2]

if __name__ == '__main__':
    scraper = AlespScrapper()
    scraper.scrape_all_subjects()
