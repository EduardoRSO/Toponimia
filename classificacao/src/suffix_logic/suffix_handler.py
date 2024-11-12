class SuffixHandler:
    def __init__(self):
        self.toponym_suffixes = [
            'ópolis', 'lândia', 'ania', 'burgo', 'grad', 'ton', 'tiba',
            'uçu', 'içá', 'pé', 'guaçu', 'gaba', 'mirim', 'ara', 'mba',
            'iba', 'una', 'oca', 'acanga', 'anga', 'assu', 'itiba',
            'quara', 'ta', 'canga', 'ar', 'ari', 'ó', 'im', 'çu',
            'cum', 'ama', 'en', 'é', 'ós', 'ito', 'ci', 'uba',
            'çuí', 'çuaba', 'ra', 'íba', 'çuã', 'péua', 'gó', 'inda',
            'da', 'hama', 'iza', 'ipé', 'iqui', 'isco', 'oá', 'çuá',
            'uí', 'oca', 'açu', 'óca', 'ango', 'ante', 'osa', 'ema',
            'pará', 'canha', 'ilma', 'ipu', 'pin', 'tama', 'xé', 'pó',
            'il', 'cue', 'ata', 'teba', 'óia', 'abo', 'pi', 'pira',
            'tai', 'pu', 'daí', 'puca', 'ã', 'çoca', 'óba', 'té',
            'porã', 'tera', 'quin', 'miró', 'ambi', 'topo', 'pari',
            'tor', 'guai', 've', 'aná', 'angu', 'porã', 'tinga',
            'tá', 'sco', 'mara', 'itó', 'ria', 'buco', 'pura',
            'tur', 'chú', 'óbia', 'alha', 'fã', 'ucum', 'bu'
        ]

    def has_suffix(self, word):
        for suffix in self.toponym_suffixes:
            if word.endswith(suffix):
                return True
        return False

if __name__ == '__main__':
    # Exemplo de uso do SuffixHandler
    suffix_handler = SuffixHandler()
    words = ["Petrópolis", "Finlândia", "Amazonas", "Curitiba", "Vale", "Aratiba"]

    for word in words:
        result = suffix_handler.has_suffix(word)
        print(f"'{word}' possui sufixo toponímico? {'Sim' if result else 'Não'}")