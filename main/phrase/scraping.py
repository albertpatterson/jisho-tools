from bs4 import BeautifulSoup
import requests

from . import utils
from .types import FuriganaValue, TextValueNeedsFurigana


def getFurigana(phrase):
    lookupResponse = requests.get(utils.getFuriganaUrl(phrase))
    lookupSoup = BeautifulSoup(lookupResponse.text, 'html.parser')

    phraseWrapper = lookupSoup.find(id='zen_bar')
    phraseItemLists = phraseWrapper.findAll('ul')

    phraseItems = []
    for phraseItemList in phraseItemLists:
        phraseItems += phraseItemList.findAll('li')

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

    return utils.combineTextAndFurigana(textValuesNeedFurigana, furiganaValues)


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
