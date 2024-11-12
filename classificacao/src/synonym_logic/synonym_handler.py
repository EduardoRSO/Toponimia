import spacy
from nltk.corpus import wordnet
import nltk # type: ignore

# Baixar dados necessários do nltk
nltk.download('omw-1.4')
nltk.download('wordnet')

# Baixar modelo de língua portuguesa do spaCy
try:
    spacy.cli.download("pt_core_news_md")
except SystemExit:
    pass

class SynonymHandler:
    def __init__(self):
        # Inicializar spaCy automaticamente
        self.nlp = spacy.load("pt_core_news_md")

    def get_synonyms(self, word):
        # Buscar sinônimos de 'word' no WordNet (adaptado para português)
        synonyms = set()
        for syn in wordnet.synsets(word, lang='por'):
            for lemma in syn.lemmas(lang='por'):
                synonyms.add(lemma.name())
        return list(synonyms)

if __name__ == '__main__':
    # Criar uma instância do SynonymHandler
    synonym_handler = SynonymHandler()
    text = "Eu visitei a metrópole brasileira Rio de Janeiro no ano passado"
    for word in text.split(' '):
        print(word, synonym_handler._check_wordnet_synonym(word))
