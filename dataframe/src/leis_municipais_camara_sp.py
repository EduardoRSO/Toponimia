#1[
#1 TITULO: LEISMUNICIPAISCAMARASP SCRAPPER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZAR O SCRAPING DE DECRETOS NO SITE LEISMUNICIPAIS.COM.BR REFERENTE À CÂMARA DE SÃO PAULO, COM BASE EM DIVERSOS ASSUNTOS
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), ASSUNTO (NA FUNÇÃO SCRAPE)
#1 SAIDAS: DADOS PROCESSADOS, LINKS EXTRAÍDOS, DECRETOS VISITADOS
#1 ROTINAS CHAMADAS: SCRAPE, BUILD_URL, PARSE_CONTENT, EXTRACT_LINKS, SCRAPE_LINKS, SCRAPE_ALL_SUBJECTS
#1]

import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from logging_logic.logging_handler import LoggingHandler
from scraping_logic.scraping_handler import ScrapingHandler

class LeisMunicipaisCamaraSpScrapper(ScrapingHandler):
    BASE_URL = "https://leismunicipais.com.br/camara/sp/sao-paulo"
    DECRETO_BASE_URL = "https://leismunicipais.com.br"
    SUBJECTS = ["Alteração", "Mudança", "Modificação", "Reforma", "Transformação", "Troca", "Reajuste", "Revisão", "Ajuste", "Correção"]
    DIRECTORY_NAME = "LeisMunicipaisCamaraSp"
    SLEEP = 15
    MAX_ERROR = 3

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE LEISMUNICIPAISCAMARASP SCRAPPER E CONFIGURA AS VARIÁVEIS INICIAIS E O DIRETÓRIO DE SALVAMENTO
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: LOGGINGHANDLER, SCRAPINGHANDLER
    #1 CHAMADO POR: LEISMUNICIPAISCAMARASP SCRAPPER
    #1 CHAMA: SCRAPINGHANDLER.__INIT__
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __INIT__
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', '__init__', show_parameters=False, show_output=False)
    def __init__(self):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI E CONFIGURA O DIRETÓRIO
        super().__init__(self.DIRECTORY_NAME)
        #2 INICIALIZA UM CONJUNTO PARA ARMAZENAR AS URLS JÁ VISITADAS
        self.visited_urls = set()
    #2]

    #1[
    #1 ROTINA: SCRAPE
    #1 FINALIDADE: REALIZAR O SCRAPING DE DECRETOS COM BASE NO ASSUNTO ESPECIFICADO
    #1 ENTRADAS: ASSUNTO (STRING)
    #1 DEPENDENCIAS: TIME, REQUESTINGHANDLER
    #1 CHAMADO POR: USUÁRIO, SCRAPE_ALL_SUBJECTS
    #1 CHAMA: BUILD_URL, MAKE_REQUEST (REQUESTINGHANDLER), PROCESS_RESPONSE, PARSE_CONTENT, EXTRACT_LINKS, SCRAPE_LINKS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: SCRAPE
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'scrape', show_parameters=False, show_output=False)
    def scrape(self, subject):
        #2 DEFINE O NÚMERO DA PÁGINA E O CONTADOR DE ERROS
        page_number = 1
        error_count = 0
        #2 ENQUANTO NÃO ATINGIR O LIMITE DE ERROS, CONTINUA FAZENDO O SCRAPING
        while error_count < self.MAX_ERROR:
            #2 CONSTROI A URL BASEADA NO ASSUNTO E NÚMERO DA PÁGINA
            url = self.build_url(subject, page_number)
            #2 FAZ A REQUISIÇÃO HTTP USANDO O HANDLER DE REQUISIÇÃO
            content = self.requesting_handler.make_request('GET', url)
            #2 PROCESSA A RESPOSTA RECEBIDA
            self.process_response(content)
            #2 SE NÃO HOUVER ERRO NA REQUISIÇÃO, PROSSEGUE COM O PARSE E EXTRAÇÃO DE LINKS
            if not content.get('error'):
                #2 ANALISA O CONTEÚDO HTML RECEBIDO
                parsed_content = self.parse_content(content['response_string'])
                #2 EXTRAI OS LINKS RELEVANTES DO CONTEÚDO HTML
                links = self.extract_links(parsed_content)
                #2 REALIZA O SCRAPING DOS LINKS ENCONTRADOS
                self.scrape_links(links)
                #2 REINICIA O CONTADOR DE ERROS
                error_count = 0
            else:
                #2 INCREMENTA O CONTADOR DE ERROS SE OCORRER UM ERRO NA REQUISIÇÃO
                error_count += 1
            #2 AUMENTA O NÚMERO DA PÁGINA E AGUARDA UM TEMPO ANTES DE CONTINUAR
            page_number += 1
            time.sleep(self.SLEEP)
    #2]

    #1[
    #1 ROTINA: BUILD_URL
    #1 FINALIDADE: CONSTRUIR A URL PARA REALIZAR A REQUISIÇÃO HTTP BASEADO NO ASSUNTO E NO NÚMERO DA PÁGINA
    #1 ENTRADAS: ASSUNTO (STRING), NÚMERO DA PÁGINA (INT)
    #1 DEPENDENCIAS: NENHUMA
    #1 CHAMADO POR: SCRAPE
    #1 CHAMA: NENHUMA
    #1]
    #2[
    #2 PSEUDOCODIGO DE: BUILD_URL
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'build_url', show_parameters=False, show_output=False)
    def build_url(self, subject, page_number):
        #2 RETORNA A URL CONSTRUÍDA COM O ASSUNTO E NÚMERO DA PÁGINA PARA A BUSCA
        return f"{self.BASE_URL}?q={subject}&page={page_number}"
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
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'parse_content', show_parameters=False, show_output=False)
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
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'extract_links', show_parameters=False, show_output=False)
    def extract_links(self, parsed_content):
        #2 EXTRAI TODOS OS LINKS QUE CONTÊM 'DECRETO' NO CAMINHO DO HREF
        return [a['href'] for a in parsed_content.find_all('a', href=True) if 'decreto' in a['href']]
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
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'scrape_links', show_parameters=False, show_output=False)
    def scrape_links(self, links):
        #2 ITERA SOBRE CADA LINK EXTRAÍDO
        for link in links:
            #2 CRIA A URL COMPLETA CONCATENANDO O LINK COM A DECRETO_BASE_URL
            full_url = f"{self.DECRETO_BASE_URL}{link}"
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
    #1 FINALIDADE: REALIZAR O SCRAPING DE TODOS OS ASSUNTOS DEFINIDOS SIMULTANEAMENTE UTILIZANDO MÚLTIPLAS THREADS
    #1 ENTRADAS: NENHUMA (UTILIZA OS ASSUNTOS DA VARIÁVEL DE CLASSE SUBJECTS)
    #1 DEPENDENCIAS: THREADPOOLEXECUTOR
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: SCRAPE (PARA CADA ASSUNTO)
    #1]
    #2[
    #2 PSEUDOCODIGO DE: SCRAPE_ALL_SUBJECTS
    @LoggingHandler.log_method('LeisMunicipaisCamaraSpScrapper', 'scrape_all_subjects', show_parameters=False, show_output=False)
    def scrape_all_subjects(self):
        #2 UTILIZA UM THREADPOOLEXECUTOR PARA PARALELIZAR O PROCESSO DE SCRAPING PARA CADA ASSUNTO EM SUBJECTS
        with ThreadPoolExecutor(max_workers=len(self.SUBJECTS)) as executor:
            #2 EXECUTA A FUNÇÃO SCRAPE PARA CADA ASSUNTO DA LISTA
            executor.map(self.scrape, self.SUBJECTS)
    #2]
if __name__ == '__main__':
    scraper = LeisMunicipaisCamaraSpScrapper()
    scraper.scrape_all_subjects()
