from src.synonym_logic.synonym_handler import SynonymHandler
from src.suffix_logic.suffix_handler import SuffixHandler
from src.lexical_similarity_logic.lexical_similarity_handler import LexicalSimilarityHandler
from src.ibge_toponyms_logic.ibge_toponyms_handler import IbgeToponymsHandler

class ClassificationWorkflowHandler:
    def __init__(self):
        # Inicializar os handlers
        self.synonym_handler = SynonymHandler()
        self.suffix_handler = SuffixHandler()
        self.similarity_handler = LexicalSimilarityHandler()
        self.ibge_toponyms_handler = IbgeToponymsHandler()

    def calculate_toponym_confidence(self, word, lemmatized_text):
        confidence_score = 0.0

        # Verificar se a palavra possui um sufixo toponímico
        if self.suffix_handler.has_suffix(word):
            confidence_score += 0.4

        # Verificar se existem palavras similares no texto
        text_similarity = self.similarity_handler.check_similarity(word, lemmatized_text.split(), 0.8)
        if text_similarity:
            confidence_score += 0.1

        # Verificar se existe similaridade com os sinonimos
        synonym_similarity = self.similarity_handler.check_similarity(word, self.synonym_handler.get_synonyms(word), 0.9)
        if synonym_similarity:
            confidence_score += 0.2
        
        # Verificar se existe similaridade com os toponimos do ibge
        ibge_toponyms_similarity = self.similarity_handler.check_similarity(word, self.ibge_toponyms_handler.get_toponyms(), 0.5)
        if ibge_toponyms_similarity:
            confidence_score += 0.2

        # Verificar se algum dos similares possui sufixo toponimo
        similar_words = text_similarity + synonym_similarity + ibge_toponyms_similarity
        if similar_words:
            similar_words_has_suffix = [word for word in similar_words if self.suffix_handler.has_suffix(word)]
            confidence_score += 0.1 * len(similar_words_has_suffix) / (len(lemmatized_text.split()) + len(similar_words))

        # Garantir que a pontuação esteja entre 0 e 1
        confidence_score = min(confidence_score, 1.0)
        return confidence_score
