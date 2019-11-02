from bs4 import BeautifulSoup
import requests
import urllib.parse


def _getFuriganaUrl(phrase):
    return 'https://jisho.org/search/'+urllib.parse.quote(phrase)


def getFurigana(phrase):
    lookupResponse = requests.get(_getFuriganaUrl(phrase))
    lookupSoup = BeautifulSoup(lookupResponse.text, 'html.parser')

    phraseWrapper = lookupSoup.find(id='zen_bar')
    phraseItems = phraseWrapper.find('ul').findAll('li')

    parsedPhraseItems = []
    for item in phraseItems:
        parsedPhraseItem = _getTextAndFurigana(item)
        parsedPhraseItems.append(parsedPhraseItem)

    parsedPhrase = ''.join(parsedPhraseItems)
    return parsedPhrase


def _getTextAndFurigana(wordItem):

    textWrapper = wordItem.find(class_='japanese_word__text_wrapper')
    textValuesNeedFurigana = _getTextElementsNeedFurigana(textWrapper)

    furiganaWrapper = wordItem.find(class_='japanese_word__furigana_wrapper')
    furiganaValues = _getFuriganaValues(furiganaWrapper)

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


class TextValueNeedsFurigana:
    def __init__(self, text, needsFurigana):
        self.text = text
        self.needsFurigana = needsFurigana

    def __str__(self):
        return 'text: "%s", needs furigana: "%s"' % (self.text, self.needsFurigana)


def _getTextElementsNeedFurigana(textWrapper):

    linkEl = textWrapper.find('a')
    if linkEl:
        textElements = linkEl.findAll('span')
    else:
        textElements = textWrapper.findAll('span')

    if not textElements:
        return [TextValueNeedsFurigana(textWrapper.text, False)]

    textElementsNeedFurigana = []
    for element in textElements:
        className = element['class']
        if len(className) != 1:
            raise Exception(
                'unexpected number of class items for japanese text element'+element)
        elif 'japanese_word__text_with_furigana' in className:
            textElementsNeedFurigana.append(
                TextValueNeedsFurigana(element.text, True))
        elif 'japanese_word__text_without_furigana' in className:
            textElementsNeedFurigana.append(
                TextValueNeedsFurigana(element.text, False))

    return textElementsNeedFurigana


class FuriganaValue:
    def __init__(self, text, furigana):
        self.text = text
        self.furigana = furigana

    def __str__(self):
        return 'text: "%s", furigana: "%s"' % (self.text, self.furigana)


def _getFuriganaValues(furiganeWrapper):

    linkEl = furiganeWrapper.find('a')
    if linkEl:
        furiganeElements = linkEl.findAll('span')
    else:
        furiganeElements = furiganeWrapper.findAll('span')

    furiganaValues = []
    for element in furiganeElements:
        dataText = element['data-text'].strip()
        invisible = 'japanese_word__furigana-invisible' in element['class']
        if dataText and not invisible:
            furiganaValues.append(FuriganaValue(
                dataText, element.text.strip()))
        else:
            furiganaValues.append(FuriganaValue(None, element.text.strip()))

    return furiganaValues
