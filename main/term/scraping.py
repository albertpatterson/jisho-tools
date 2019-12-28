from bs4 import BeautifulSoup
import requests
from . import utils
from .types import Definition


def getDefinitions(term):
    lookupResponse = requests.get(utils.getDefinitionUrl(term))
    lookupSoup = BeautifulSoup(lookupResponse.text, 'html.parser')

    primary = lookupSoup.find(id='primary')
    exactBlock = _matchSingleClass(primary, 'exact_block')
    matches = exactBlock.findAll(class_='concept_light')

    definitions = []

    for match in matches:
        definitions.append(_extractEntryParts(match))

    return sorted(definitions, key=lambda d: d.kanji != term)


def _extractEntryParts(entry):
    kanji = _extractKanji(entry)
    furigana = _extractFurigana(entry)
    definition = _extractDefinition(entry)

    return Definition(kanji, furigana, definition)


def _extractKanji(entry):
    rep = _matchSingleClass(entry, 'concept_light-representation')

    textParts = _extractTextParts(rep)
    return ''.join(textParts)


def _extractFurigana(entry):
    rep = _matchSingleClass(entry, 'concept_light-representation')
    textParts = _extractTextParts(rep)
    furiganaParts = _extractFuriganaParts(rep)
    return utils.combineTextAndFurigana(textParts, furiganaParts)


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
