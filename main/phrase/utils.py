import urllib.parse


def getFuriganaUrl(phrase):
    return 'https://jisho.org/search/'+urllib.parse.quote(phrase)


def combineTextAndFurigana(textValuesNeedFurigana, furiganaValues):
    furiganaValueCount = len(furiganaValues)

    furiganaValueCount = len(furiganaValues)

    if furiganaValueCount == 0:
        if len(textValuesNeedFurigana) == 1:
            textValueNeedsFurigana = textValuesNeedFurigana[0]
            if not textValueNeedsFurigana.needsFurigana:
                return textValueNeedsFurigana.text
            else:
                raise Exception(
                    'Text needs furigana but none found. '+textValueNeedsFurigana)
        else:
            raise Exception(
                'Multiple text items found but no furigana found'+textValuesNeedFurigana)

    if len(textValuesNeedFurigana) != furiganaValueCount:
        raise Exception('text and furigana value count mismatch')

    textAndFuriganaValues = []
    for idx in range(furiganaValueCount):
        textValueNeedsFurigana = textValuesNeedFurigana[idx]
        furiganaValue = furiganaValues[idx]

        if not textValueNeedsFurigana.text:
            raise Exception('invalid text value '+str(textValueNeedsFurigana))

        if textValueNeedsFurigana.needsFurigana:
            if textValueNeedsFurigana.text != furiganaValue.text:
                raise Exception('furigana text mismatch ' +
                                str(textValueNeedsFurigana)+' '+str(furiganaValue))

            textAndFuriganaValues.append(
                '{%s,%s}' % (furiganaValue.text, furiganaValue.furigana))

        else:
            if furiganaValue.text:
                raise Exception('text expected to need furigana ' +
                                '\ntextValueNeedsFurigana: ' + str(textValueNeedsFurigana) +
                                '\nfuriganaValue: ' + str(furiganaValue))

            textAndFuriganaValues.append(textValueNeedsFurigana.text)

    return ''.join(textAndFuriganaValues)
