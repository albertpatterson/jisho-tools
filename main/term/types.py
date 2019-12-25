class Definition:
    def __init__(self, kanji, furigana, definition):
        self.kanji = kanji
        self.furigana = furigana
        self.definition = definition

    def __str__(self):
        definitions = '\n'.join(map(lambda d: '\t'+d, self.definition))
        return 'kanji: %s\nfurigana: %s\ndefinitions:\n%s' % (self.kanji, self.furigana, definitions)
