#1[
#1 TITULO: TOPONYMHANDLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 07/10/2024
#1 VERSAO: 1
#1 FINALIDADE: LEMATIZAR TEXTOS E EXTRAIR TOPÔNIMOS (NOMES DE LOCAIS) USANDO PADRÕES DEFINIDOS
#1 ENTRADAS: NOME DO DIRETÓRIO (NO CONSTRUTOR), TEXTO (NA FUNÇÃO LEMMATIZE_AND_EXTRACT_TOPONYMS)
#1 SAIDAS: TEXTO LEMATIZADO E LISTA DE TOPÔNIMOS EXTRAÍDOS
#1 ROTINAS CHAMADAS: _ADD_PATTERNS, LEMMATIZE_AND_EXTRACT_TOPONYMS
#1]

import re
import spacy
from spacy.matcher import Matcher
from logging_logic.logging_handler import LoggingHandler

class ToponymHandler(LoggingHandler):
    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE TOPONYMHANDLER E CONFIGURA O PROCESSAMENTO DE LINGUAGEM NATURAL E PADRÕES DE TOPÔNIMOS
    #1 ENTRADAS: NOME DO DIRETÓRIO (STRING)
    #1 DEPENDENCIAS: SPACY, MATCHER, LOGGINGHANDLER
    #1 CHAMADO POR: TOPONYMHANDLER
    #1 CHAMA: LOGGINGHANDLER.__INIT__, SPACY.LOAD, MATCHER
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __INIT__
    def __init__(self, directory_name):
        #2 CHAMA O CONSTRUTOR DA CLASSE PAI E INICIALIZA O DIRETÓRIO
        super().__init__(directory_name)
        #2 ARMAZENA O NOME DO DIRETÓRIO
        self.directory_name = directory_name
        #2 CARREGA O MODELO DE LINGUAGEM NATURAL EM PORTUGUÊS USANDO SPACY
        self.nlp = spacy.load("pt_core_news_sm")
        #2 INICIALIZA O MATCHER (PARA DETECTAR PADRÕES DE TOPÔNIMOS)
        self.matcher = Matcher(self.nlp.vocab)
        #2 CHAMA A FUNÇÃO PARA ADICIONAR PADRÕES AO MATCHER
        self._add_patterns()
    #2]

    #1[
    #1 ROTINA: _ADD_PATTERNS
    #1 FINALIDADE: ADICIONA PADRÕES DE TOPÔNIMOS AO MATCHER USANDO NOMES PRÓPRIOS E PALAVRAS-CHAVE RELACIONADAS A LOCAIS
    #1 ENTRADAS: NENHUMA
    #1 DEPENDENCIAS: SPACY, RE
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: MATCHER.ADD
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _ADD_PATTERNS
    @LoggingHandler.log_method("ToponymHandler", "_add_patterns")
    def _add_patterns(self):
        #2 DEFINE OS TERMOS RELACIONADOS A LOCAIS E SUAS ABREVIAÇÕES
        location_keywords = [
            "AV", "AV.", "AVENIDA",
            "R", "R.", "RUA",
            "ESTRADA", "PONTE", "AEROPORTO", "CIDADE", "MUNICÍPIO",
            "PRAÇA", "RODOVIA", "TRAVESSA", "BAIRRO", "DISTRITO", "LAGO", "RIO", "VILA"
        ]

        #2 DEFINE PADRÕES FIXOS QUE CORRESPONDEM A NOMES PRÓPRIOS E ESTRUTURAS COMUNS EM NOMES DE LOCAIS
        base_patterns = [
            #2 EX: SÃO PAULO
            [{"POS": "PROPN"}],
            #2 EX: RIO DE JANEIRO
            [{"POS": "PROPN"}, {"POS": "ADP"}, {"POS": "PROPN"}],
            #2 EX: CIDADE DE SÃO PAULO
            [{"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}],
            #2 EX: VILA NOVA DE GAIA
            [{"POS": "NOUN"}, {"POS": "ADJ"}, {"POS": "ADP"}, {"POS": "PROPN"}],
            #2 EX: SÃO PEDRO E SÃO PAULO
            [{"POS": "PROPN"}, {"POS": "CCONJ"}, {"POS": "PROPN"}],
            #2 EX: O RIO DE JANEIRO
            [{"POS": "DET"}, {"POS": "PROPN"}, {"POS": "ADP"}, {"POS": "PROPN"}],
            #2 EX: A CIDADE DE SÃO PAULO
            [{"POS": "DET"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}],
            #2 EX: A CIDADE DE SÃO PAULO E RIO DE JANEIRO
            [{"POS": "DET"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}, {"POS": "CCONJ"}, {"POS": "PROPN"}],
            #2 EX: ALOYSIO NUNES
            [{"POS": "PROPN"}, {"POS": "PROPN"}],
            #2 EX: PEDRO ÁLVARES CABRAL
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
            #2 EX: ALOYSIO NUNES FERREIRA FILHO
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],
        ]

        #2 DEFINE PADRÕES PARA NOMES PRÓPRIOS COM HÍFEN
        hyphenated_patterns = [
            #2 DOIS NOMES PRÓPRIOS COM HÍFEN EX: PEDRO ÁLVARES-CABRAL
            [{"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}],  
            #2 TRÊS NOMES PRÓPRIOS COM UM HÍFEN EX: PEDRO ÁLVARES-CABRAL FILHO
            [{"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"POS": "PROPN"}],   
            #2 DOIS NOMES PRÓPRIOS SEGUIDOS DE UM HÍFEN E MAIS DOIS NOMES PRÓPRIOS EX: JOÃO PAULO-SILVA
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}],   
            #2 TRÊS NOMES PRÓPRIOS COM TRES HÍFENS EX: JOÃO-PAULO-SILVA
            [{"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}],  
            #2 TRÊS NOMES PRÓPRIOS COM DOIS HÍFENS EX: JOÃO-PAULO-SILVA FILHO
            [{"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"POS": "PROPN"}],  
            #2 QUATRO NOMES PRÓPRIOS COM DOIS HÍFENS EX: JOÃO-PAULO-SILVA-SANTOS
            [{"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}, {"ORTH": "-"}, {"POS": "PROPN"}],  
        ]

        patterns = []

        #2 ADICIONA OS PADRÕES FIXOS AO MATCHER
        patterns.extend(base_patterns)

        #2 ADICIONA VARIAÇÕES DOS PADRÕES USANDO PALAVRAS-CHAVE DE LOCAIS
        for keyword in location_keywords:
            for pattern in base_patterns:
                #2 CADA PADRÃO BASE É PRECEDIDO POR UMA PALAVRA-CHAVE DE LOCAL
                patterns.append([{"TEXT": keyword}] + pattern)

            #2 ADICIONA VARIAÇÕES COM HÍFENS PARA CADA PALAVRA-CHAVE
            for hyphen_pattern in hyphenated_patterns:
                patterns.append([{"TEXT": keyword}] + hyphen_pattern)

        #2 ADICIONA OS PADRÕES COM HÍFEN AO MATCHER
        patterns.extend(hyphenated_patterns)

        #2 ADICIONA TODOS OS PADRÕES AO MATCHER
        for pattern in patterns:
            self.matcher.add("TOPONIMO", [pattern])
    #2]

    #1[
    #1 ROTINA: LEMMATIZE_AND_EXTRACT_TOPONYMS
    #1 FINALIDADE: LEMATIZA O TEXTO E EXTRAI OS TOPÔNIMOS USANDO O MATCHER
    #1 ENTRADAS: TEXTO (STRING)
    #1 DEPENDENCIAS: SPACY, MATCHER
    #1 CHAMADO POR: USUÁRIO
    #1 CHAMA: MATCHER, NLP
    #1]
    #2[
    #2 PSEUDOCODIGO DE: LEMMATIZE_AND_EXTRACT_TOPONYMS
    @LoggingHandler.log_method("ToponymHandler", "lemmatize_and_extract_toponyms")
    def lemmatize_and_extract_toponyms(self, text):
        try:
            #2 PROCESSA O TEXTO USANDO O MODELO NLP
            doc = self.nlp(text)
            #2 LEMATIZA CADA TOKEN DO TEXTO
            lemmatized_text = " ".join([token.lemma_ for token in doc])
            #2 ENCONTRA OS PADRÕES CORRESPONDENTES AOS TOPÔNIMOS NO TEXTO
            matches = self.matcher(doc)
            #2 EXTRAI OS TOPÔNIMOS IDENTIFICADOS
            toponyms = [doc[start:end].text for match_id, start, end in matches]
            #2 RETORNA O TEXTO LEMATIZADO E OS TOPÔNIMOS COMO UMA STRING SEPARADA POR VÍRGULAS
            return lemmatized_text, ",".join(toponyms)
        except Exception as e:
            #2 RETORNA STRINGS VAZIAS EM CASO DE ERRO
            return "", ""
    #2]
