import spacy
from nltk.corpus import wordnet
import nltk # type: ignore

# Baixar dados necessários do nltk, caso ainda não estejam disponíveis
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Verificar se o modelo de língua portuguesa do spaCy já está baixado
model_name = "pt_core_news_md"
if not spacy.util.is_package(model_name):
    try:
        spacy.cli.download(model_name)
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
