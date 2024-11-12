from src.synonym_logic.synonym_handler import SynonymHandler
from src.suffix_logic.suffix_handler import SuffixHandler
from src.lexical_similarity_logic.lexical_similarity_handler import LexicalSimilarityHandler

class ClassificationWorkflowHandler:
    def __init__(self):
        # Inicializar os handlers
        self.synonym_handler = SynonymHandler()
        self.suffix_handler = SuffixHandler()
        self.similarity_handler = LexicalSimilarityHandler()

    def calculate_toponym_confidence(self, word, lemmatized_text):
        confidence_score = 0.0

        # Verificar se a palavra possui um sufixo toponímico
        if self.suffix_handler.has_suffix(word):
            confidence_score += 0.4

        # Obter sinônimos da palavra
        synonyms = self.synonym_handler.get_synonyms(word)

        # Verificar se algum sinônimo está presente no texto lematizado
        for synonym in synonyms:
            if synonym in lemmatized_text.split():
                confidence_score += 0.3
                break

        # Calcular similaridade léxica entre a palavra e as palavras do texto lematizado
        similar_words = self.similarity_handler.check_similarity(word, lemmatized_text.split())
        if similar_words:
            # Se houverem palavras similares, verifica se possuem sufixo toponimico
            similar_words_has_suffix = [word for word in similar_words if self.suffix_handler.has_suffix(word)]
            confidence_score += 0.3 * len(similar_words_has_suffix) / (len(lemmatized_text.split()) + len(similar_words))

        # Garantir que a pontuação esteja entre 0 e 1
        confidence_score = min(confidence_score, 1.0)

        return confidence_score
