class TextValueNeedsFurigana:
    def __init__(self, text, needsFurigana):
        self.text = text
        self.needsFurigana = needsFurigana

    def __str__(self):
        return 'text: "%s", needs furigana: "%s"' % (self.text, self.needsFurigana)


class FuriganaValue:
    def __init__(self, text, furigana):
        self.text = text
        self.furigana = furigana

    def __str__(self):
        return 'text: "%s", furigana: "%s"' % (self.text, self.furigana)
