from bs4 import BeautifulSoup
import requests


def _getDetailsUrl(kanji):
    return 'https://jisho.org/search/' + kanji + '%20%23kanji'


def getDetails(kanji):
    lookupUrl = _getDetailsUrl(kanji)
    lookupResponse = requests.get(lookupUrl)
    lookupSoup = BeautifulSoup(lookupResponse.text, 'html.parser')

    meaningText = lookupSoup.find(
        class_='kanji-details__main-meanings').text.strip()
    # print(meaningText)

    kanjiDetails = lookupSoup.find(
        class_='kanji-details__main-readings')
    # print(kanjiDetails)

    kunyomiEntry = kanjiDetails.find(
        class_='dictionary_entry kun_yomi')
    # print(kunyomiEntry)

    kunyomiText = kunyomiEntry.find(
        class_='kanji-details__main-readings-list').text.strip() if not kunyomiEntry is None else ''
    # print(kunyomiText)

    onyomiEntry = kanjiDetails.find(
        class_='dictionary_entry on_yomi')
    # print(onyomiEntry)

    onyomiText = onyomiEntry.find(
        class_='kanji-details__main-readings-list').text.strip() if not onyomiEntry is None else ''

    # print(onyomiText)

    return (meaningText, kunyomiText, onyomiText)
