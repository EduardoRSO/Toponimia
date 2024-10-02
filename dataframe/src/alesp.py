import time
import requests
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

    @LoggingHandler.log_method('AlespScrapper', '__init__', show_parameters=False, show_output=False)
    def __init__(self):
        super().__init__(self.DIRECTORY_NAME)
        self.visited_urls = set()

    @LoggingHandler.log_method('AlespScrapper', 'scrape', show_parameters=False, show_output=False)
    def scrape(self, subject):
        escaped_subject = urllib.parse.quote(subject)
        decoded_subject = urllib.parse.unquote(escaped_subject)
        page_number = 1
        error_count = 0
        while error_count < self.MAX_ERROR:
            url = self.build_url(page_number, escaped_subject, decoded_subject)
            content = self.requesting_handler.make_request('GET', url)
            self.process_response(content)
            if not content.get('error'):
                parsed_content = self.parse_content(content['response_string'])
                links = self.extract_links(parsed_content)
                self.scrape_links(links)
                error_count = 0
            else:
                error_count += 1
            page_number += 1
            time.sleep(self.SLEEP)

    @LoggingHandler.log_method('AlespScrapper', 'build_url', show_parameters=False, show_output=False)
    def build_url(self, page_number, escaped_subject, decoded_subject):
        return (f"{self.BASE_URL}/resultados?page={page_number}&size=10&tipoPesquisa=E&"
                f"buscaLivreEscape=&buscaLivreDecode=&_idsTipoNorma=1&idsTipoNorma=9&"
                f"idsTipoNorma=2&idsTipoNorma=55&idsTipoNorma=3&idsTipoNorma=28&"
                f"idsTipoNorma=25&idsTipoNorma=1&idsTipoNorma=19&idsTipoNorma=14&"
                f"idsTipoNorma=12&idsTipoNorma=21&idsTipoNorma=22&idsTipoNorma=23&"
                f"idsTipoNorma=59&nuNorma=&ano=&complemento=&dtNormaInicio=&dtNormaFim=&"
                f"idTipoSituacao=0&_idsTema=1&palavraChaveEscape={escaped_subject}&"
                f"palavraChaveDecode={decoded_subject}&_idsAutorPropositura=1&_temQuestionamentos=on")

    @LoggingHandler.log_method('AlespScrapper', 'parse_content', show_parameters=False, show_output=False)
    def parse_content(self, content):
        return BeautifulSoup(content, 'html.parser')

    @LoggingHandler.log_method('AlespScrapper', 'extract_links', show_parameters=False, show_output=False)
    def extract_links(self, parsed_content):
        return [a['href'] for a in parsed_content.find_all('a', href=True) if 'norma' in a['href']]

    @LoggingHandler.log_method('AlespScrapper', 'scrape_links', show_parameters=False, show_output=False)
    def scrape_links(self, links):
        for link in links:
            full_url = f"{self.NORMA_BASE_URL}{link}"
            if full_url not in self.visited_urls:
                self.visited_urls.add(full_url)
                content = self.requesting_handler.make_request('GET', full_url)
                self.process_response(content)
                time.sleep(self.SLEEP)

    @LoggingHandler.log_method('AlespScrapper', 'scrape_all_subjects', show_parameters=False, show_output=False)
    def scrape_all_subjects(self):
        with ThreadPoolExecutor(max_workers=len(self.SUBJECTS)) as executor:
            executor.map(self.scrape, self.SUBJECTS)

if __name__ == '__main__':
    scraper = AlespScrapper()
    scraper.scrape_all_subjects()
