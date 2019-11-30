import pytest
from main import term


valid_kanji_furigana_combined = [
    # single kanji, single furigana
    [['夏'], ['なつ'], '{夏,なつ}'],
    # mulitiple kanji, each with a furigana
    [['大', '丈', '夫'], ['だい', 'じょう', 'ぶ'], '{大,だい}{丈,じょう}{夫,ぶ}'],
    # multiple kanji as single element, single furigana
    [['今日'], ['きょう'], '{今日,きょう}'],
    # multiple kanji, single furigana
    [['今', '日'], ['きょう'], '{今日,きょう}'],
    # single kanji with hirigana, all matched
    [['楽', 'し', 'い'], ['たの', '', ''], '{楽,たの}しい'],
    # hirigana first
    [['ご', '飯'], ['', 'はん'], 'ご{飯,はん}'],
    # hirigana in middle
    [['下', 'の', '名', '前'], ['した', '', 'な', 'まえ'], '{下,した}の{名,な}{前,まえ}'],
    # no kanji
    [['え', 'え'], ['', ''], 'ええ'],
    # # weird stuff encountered
    [['学区'], ['がっく', None], '{学区,がっく}'],

]


@pytest.mark.parametrize("kanji,furigana,combined", valid_kanji_furigana_combined)
def test_combineTextAndFurigana_valid(kanji, furigana, combined):
    assert term._combineTextAndFurigana(kanji, furigana) == combined


invalid_kanji_furigana = [
    # single kanji, missing furigana
    [['夏'], []],
    # single kanji, empty furigana
    [['夏'], ['']],
    # single kanji, invalid furigana
    [['夏'], ['pickles']],
    # missing kanji, single furigana
    [[], ['なつ']],
    # empty kanji, single furigana
    [[''], ['なつ']],
]


@pytest.mark.parametrize("kanji,furigana", invalid_kanji_furigana)
def test_combineTextAndFurigana_invalid(kanji, furigana):
    with pytest.raises(Exception) as exception:
        term._combineTextAndFurigana(kanji, furigana)

    assert exception != None
