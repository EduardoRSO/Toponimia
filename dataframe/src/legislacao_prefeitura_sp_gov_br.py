import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from logging_logic.logging_handler import LoggingHandler
from scraping_logic.scraping_handler import ScrapingHandler

class LegislacaoPrefeituraSpGovBrScrapper(ScrapingHandler):
    BASE_URL = "https://legislacao.prefeitura.sp.gov.br"
    SUBJECTS = ["Alteração", "Mudança", "Modificação", "Reforma", "Transformação", "Troca", "Reajuste", "Revisão", "Ajuste", "Correção"]
    DIRECTORY_NAME = "LegislacaoprefeituraSpGovBr"
    SLEEP = 15
    MAX_ERROR = 3

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', '__init__', show_parameters=False, show_output=False)
    def __init__(self):
        super().__init__(self.DIRECTORY_NAME)
        self.visited_urls = set()

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'scrape', show_parameters=False, show_output=False)
    def scrape(self, subject):
        page_number = 2
        error_count = 0
        while error_count < self.MAX_ERROR:
            url = self.build_url(subject, page_number)
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

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'build_url', show_parameters=False, show_output=False)
    def build_url(self, subject, page_number):
        return f"{self.BASE_URL}/busca/pg/{page_number}?assunto={subject}"

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'parse_content', show_parameters=False, show_output=False)
    def parse_content(self, content):
        return BeautifulSoup(content, 'html.parser')

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'extract_links', show_parameters=False, show_output=False)
    def extract_links(self, parsed_content):
        return [a['href'] for a in parsed_content.find_all('a', href=True) if 'leis' in a['href']]

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'scrape_links', show_parameters=False, show_output=False)
    def scrape_links(self, links):
        for link in links:
            full_url = f"{self.BASE_URL}{link}"
            if full_url not in self.visited_urls:
                self.visited_urls.add(full_url)
                content = self.requesting_handler.make_request('GET', full_url)
                self.process_response(content)
                time.sleep(self.SLEEP)

    @LoggingHandler.log_method('LegislacaoPrefeituraSpGovBrScrapper', 'scrape_all_subjects', show_parameters=False, show_output=False)
    def scrape_all_subjects(self):
        with ThreadPoolExecutor(max_workers=len(self.SUBJECTS)) as executor:
            executor.map(self.scrape, self.SUBJECTS)

if __name__ == '__main__':
    scraper = LegislacaoPrefeituraSpGovBrScrapper()
    scraper.scrape_all_subjects()