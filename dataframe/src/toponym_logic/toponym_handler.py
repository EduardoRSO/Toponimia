import spacy
from spacy.matcher import Matcher
from logging_logic.logging_handler import LoggingHandler

class ToponymHandler(LoggingHandler):
    def __init__(self, directory_name):
        super().__init__(directory_name)
        self.directory_name = directory_name
        self.nlp = spacy.load("pt_core_news_sm")
        self.matcher = Matcher(self.nlp.vocab)
        self._add_patterns()

    @LoggingHandler.log_method("ToponymHandler", "_add_patterns")
    def _add_patterns(self):
        # Definindo os termos que correspondem a diferentes tipos de locais e suas abreviações
        location_keywords = [
            "av", "av.", "avenida",
            "r", "r.", "rua",
            "estrada", "ponte", "aeroporto", "cidade", "município",
            "praça", "rodovia", "travessa", "bairro", "distrito", "lago", "rio", "vila"
        ]

        # Padrões fixos que já existiam
        base_patterns = [
            [{"POS": "PROPN"}],  # Ex: São Paulo
            [{"POS": "PROPN"}, {"POS": "ADP"}, {"POS": "PROPN"}],  # Ex: Rio de Janeiro
            [{"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}],  # Ex: Cidade de São Paulo
            [{"POS": "NOUN"}, {"POS": "ADJ"}, {"POS": "ADP"}, {"POS": "PROPN"}],  # Ex: Vila Nova de Gaia
            [{"POS": "PROPN"}, {"POS": "CCONJ"}, {"POS": "PROPN"}],  # Ex: São Pedro e São Paulo
            [{"POS": "DET"}, {"POS": "PROPN"}, {"POS": "ADP"}, {"POS": "PROPN"}],  # Ex: O Rio de Janeiro
            [{"POS": "DET"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}],  # Ex: A cidade de São Paulo
            [{"POS": "DET"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}, {"POS": "CCONJ"}, {"POS": "PROPN"}],  # Ex: A cidade de São Paulo e Rio de Janeiro
            [{"POS": "PROPN"}, {"POS": "PROPN"}],  # Ex: Aloysio Nunes
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],  # Ex: Pedro Álvares Cabral
            [{"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}, {"POS": "PROPN"}],  # Ex: Aloysio Nunes Ferreira Filho
        ]

        patterns = []

        # Adiciona os padrões fixos
        patterns.extend(base_patterns)

        # Adiciona as variações dos padrões com location_keywords
        for keyword in location_keywords:
            for pattern in base_patterns:
                # Cada padrão do base_patterns agora é precedido por uma location_keyword
                patterns.append([{"LOWER": {"IN": [keyword]}}] + pattern)

        # Adicionando os padrões ao matcher
        for pattern in patterns:
            self.matcher.add("Toponimo", [pattern])

            
    @LoggingHandler.log_method("ToponymHandler", "lemmatize_and_extract_toponyms")
    def lemmatize_and_extract_toponyms(self, text):
        try:
            doc = self.nlp(text)
            lemmatized_text = " ".join([token.lemma_ for token in doc])
            matches = self.matcher(doc)
            toponyms = [doc[start:end].text for match_id, start, end in matches]
            return lemmatized_text, ",".join(toponyms)
        except Exception as e:
            return "", ""
