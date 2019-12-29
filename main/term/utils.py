def getDefinitionUrl(term):
    return 'https://jisho.org/search/%s' % term


def combineTextAndFurigana(kanjiParts, furiganaParts):

    # catch if kanjiParts or furiganaParts are individually invalid
    if len(kanjiParts) == 0:
        raise Exception('Missing kanji')
    elif len(furiganaParts) == 0:
        raise Exception('Missing furigana')
    elif not _isValidFurigana(furiganaParts):
        raise Exception('invalid furigana %s' % str(furiganaParts))
    elif not _isValidKanji(kanjiParts):
        raise Exception('invalid kanji %s' % str(kanjiParts))

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
