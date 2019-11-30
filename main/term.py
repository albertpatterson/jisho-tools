from bs4 import BeautifulSoup
import requests


def _getDefinitionUrl(term):
    return 'https://jisho.org/search/%s' % term


class Definition:
    def __init__(self, kanji, furigana, definition):
        self.kanji = kanji
        self.furigana = furigana
        self.definition = definition

    def __str__(self):
        definitions = '\n'.join(map(lambda d: '\t'+d, self.definition))
        return 'kanji: %s\nfurigana: %s\ndefinitions:\n%s' % (self.kanji, self.furigana, definitions)


def getDefinitions(term):
    lookupResponse = requests.get(_getDefinitionUrl(term))
    lookupSoup = BeautifulSoup(lookupResponse.text, 'html.parser')

    primary = lookupSoup.find(id='primary')
    exactBlock = _matchSingleClass(primary, 'exact_block')
    matches = exactBlock.findAll(class_='concept_light')

    # print(matches)

    definitions = []

    for match in matches:
        # print(match)
        definitions.append(_extractEntryParts(match))

    return definitions

    # lookup term
    # get all exact matches
    # return as list

    # pass


def _extractEntryParts(entry):
    kanji = _extractKanji(entry)
    furigana = _extractFurigana(entry)
    definition = _extractDefinition(entry)

    return Definition(kanji, furigana, definition)


def _extractKanji(entry):
    rep = _matchSingleClass(entry, 'concept_light-representation')
    # repTextEl = _matchSingleClass(rep, 'text')
    # return repTextEl.text.strip()
    textParts = _extractTextParts(rep)
    return ''.join(textParts)


def _extractFurigana(entry):
    rep = _matchSingleClass(entry, 'concept_light-representation')
    textParts = _extractTextParts(rep)
    furiganaParts = _extractFuriganaParts(rep)
    return _combineTextAndFurigana(textParts, furiganaParts)


def _combineTextAndFurigana(kanjiParts, furiganaParts):

    # catch if kanjiParts or furiganaParts are individually invalid
    if len(kanjiParts) == 0:
        raise Exception('Missing kanji')
    elif len(furiganaParts) == 0:
        raise Exception('Missing furigana')
    elif not _isValidFurigana(furiganaParts):
        raise Exception('invalid furigana')
    elif not _isValidKanji(kanjiParts):
        raise Exception('invalid kanji')

    # attempt to match lengths
    if len(kanjiParts) != len(furiganaParts):

        # try to make one big furigana
        if len(furiganaParts) == 1 and _isAllkanji(kanjiParts):
            kanjiParts = [''.join(kanjiParts)]

        # remove unneeded Nones
        if len(furiganaParts) > len(kanjiParts) and _allNone(furiganaParts[len(kanjiParts):]):
            furiganaParts = furiganaParts[0:len(kanjiParts)]

        else:
            # try to split the kanji parts into single char parts
            singleCharKanjiParts = []
            for kanjiPart in kanjiParts:
                if len(kanjiPart) > 0:
                    singleCharKanjiParts += list(kanjiPart)
                else:
                    singleCharKanjiParts.append(kanjiPart)

            if len(singleCharKanjiParts) == len(furiganaParts):
                kanjiParts = singleCharKanjiParts

    if len(kanjiParts) != len(furiganaParts):
        raise Exception(
            'furigana and text length mismatch and not convertable')

    parts = []
    for idx in range(len(kanjiParts)):
        if furiganaParts[idx]:
            parts.append('{%s,%s}' % (kanjiParts[idx], furiganaParts[idx]))
        elif isHirigana(kanjiParts[idx]) or isKatakana(kanjiParts[idx]):
            parts.append(kanjiParts[idx])
        else:
            raise Exception('invalid furigana')

    return ''.join(parts)


def _extractTextParts(rep):
    return _extractTextFuriganaParts(rep, 'text')


def _extractFuriganaParts(rep):
    return _extractTextFuriganaParts(rep, 'furigana')


def _extractTextFuriganaParts(rep, class_):
    wrapper = _matchSingleClass(rep, class_)
    els = wrapper.children

    parts = []
    for el in els:
        elStr = el.string
        if not elStr:
            parts.append(None)
        else:
            stripped = elStr.strip()
            if len(stripped) > 0:
                parts.append(stripped)

    return parts


def _extractDefinition(entry):
    rep = _matchSingleClass(entry, 'concept_light-meanings')
    meaningWrappers = rep.findAll(class_='meaning-wrapper')
    meanings = []
    for meaningWrapper in meaningWrappers:
        meaning = _matchSingleClass(meaningWrapper, 'meaning-meaning')
        if meaning:

            meanings.append(meaning.text)

    return meanings


def _matchSingleClass(soup, class_):
    reps = soup.findAll(class_=class_)
    nReps = len(reps)
    if nReps == 0:
        return None
    if not nReps == 1:
        raise Exception(
            'invalid %s items found. Expected 1 but found %d' % (class_, nReps))

    return reps[0]


# def _formatKanjiAndFurigana(text, furigana):
#     # if(len(text) == 1):
#     #     text = list(text[0])

#     if(_isValidFurigana(text, furigana)):
#         formats = []
#         hirigana = []
#         for i in range(len(text)):
#             if(furigana[i]):
#                 appendage = '{%s,%s}' % (text[i], furigana[i])
#                 formats.append(appendage)
#             # formats.append(text[i])
#             #     formats += ['{', furigana[i], '}']
#                 hirigana += furigana[i]
#             else:
#                 formats.append(text[i])
#                 hirigana += text[i]

#         return (True, ''.join(formats), ''.join(hirigana))
#     else:
#         kanji = ''.join(filter(lambda x: x, text))
#         hirigana = ''.join(filter(lambda x: x, furigana))
#         return (False, '{%s,%s}' % (kanji, hirigana), 'None')


# def _isValidFurigana(text, furigana):
#     valid = len(text) == len(furigana)
#     for item in text:
#         valid = valid and len(item) == 1

#     return valid


# def _getWordFurigana(wordTextWrapper):
#     furiganaWrapper = _matchSingleClass(wordTextWrapper, 'furigana')

#     if not furiganaWrapper:
#         return None

#     furigana = []
#     for element in furiganaWrapper.children:
#         str = element.string.strip()
#         furigana.append(str)

#     # first and last are just newlines
#     return furigana


# def _getWordText(wordTextWrapper):
#     textWrapper = _matchSingleClass(wordTextWrapper, 'text')

#     if not textWrapper:
#         return None

#     text = []
#     for element in textWrapper.children:
#         str = element.string.strip()
#         text.append(str)

#     return text

def isHirigana(char):
    # see https://www.ssec.wisc.edu/~tomw/java/unicode.html#x3040
    charo = ord(char)
    return charo >= 12353 and charo <= 12446


def isKatakana(char):
    # see https://www.ssec.wisc.edu/~tomw/java/unicode.html#x3040
    charo = ord(char)
    return charo >= 12449 and charo <= 12542


def _anyPartEmpty(parts):
    assert isinstance(parts, list)
    for part in parts:
        assert isinstance(part, str)
        if not part:
            return True
    return False


def _allCharsAreHiraganaOrEmpty(parts):
    assert isinstance(parts, list)
    for part in parts:
        assert isinstance(part, str)
        for char in part:
            if not isHirigana(char):
                return False
    return True


def _anyCharsAreHiraganaOrKatakana(parts):
    assert isinstance(parts, list)
    for part in parts:
        assert isinstance(part, str)
        for char in part:
            if isHirigana(char) or isKatakana(char):
                return True
    return False


def _isValidFurigana(parts):
    assert isinstance(parts, list)
    for part in parts:

        if part == None:
            continue

        assert isinstance(part, str)
        for char in part:
            if not isHirigana(char):
                return False
    return True


def _isValidKanji(parts):
    return not _anyPartEmpty(parts)


def _allNone(values):
    for value in values:
        if not value == None:
            return False
    return True


def _isAllkanji(parts):
    if _anyPartEmpty(parts):
        return False

    if _anyCharsAreHiraganaOrKatakana(parts):
        return False

    return True
