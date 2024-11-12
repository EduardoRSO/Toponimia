import spacy

class LexicalSimilarityHandler:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_md")
        self.threshold = 0.5

    def check_similarity(self, word, synonyms):
        similar_words = []
        word_doc = self.nlp(word)

        for synonym in synonyms:
            synonym_doc = self.nlp(synonym)
            similarity = word_doc.similarity(synonym_doc)
            if similarity > self.threshold:
                similar_words.append(synonym)

        return similar_words

if __name__ == "__main__":
    # Criar uma instância do handler
    similarity_handler = LexicalSimilarityHandler()

    # Palavra de teste
    word = "cidade"
    # Lista de sinônimos para verificar
    synonyms = ["metrópole", "aldeia", "vila", "estado", "capital", "país"]

    # Verificar a similaridade entre a palavra e os sinônimos
    similar_words = similarity_handler.check_similarity(word, synonyms)

    # Imprimir resultados
    print(f"Palavra: '{word}'")
    print(f"Sinônimos fornecidos: {', '.join(synonyms)}")
    print(f"Palavras similares a '{word}' (similaridade > 0.5): {', '.join(similar_words) if similar_words else 'Nenhuma'}")
