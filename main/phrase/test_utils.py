import pytest
from main.phrase import utils
from main.phrase.types import FuriganaValue, TextValueNeedsFurigana

valid_kanji_furigana_combined = [
    # single hirigana, needs no furigana
    [
        [
            TextValueNeedsFurigana('ご', False)
        ],
        [],
        'ご'
    ],
    # single kanji, needs furigana
    [
        [
            TextValueNeedsFurigana('夏', True)
        ],
        [
            FuriganaValue('夏', 'なつ')
        ],
        '{夏,なつ}'
    ],
    # mulitiple kanji, each with a furigana
    [
        [
            TextValueNeedsFurigana('大', True),
            TextValueNeedsFurigana('丈', True),
            TextValueNeedsFurigana('夫', True),
        ],
        [
            FuriganaValue('大', 'だい'),
            FuriganaValue('丈', 'じょう'),
            FuriganaValue('夫', 'ぶ'),
        ],
        '{大,だい}{丈,じょう}{夫,ぶ}',
    ],
    # multiple kanji as single element, single furigana
    [
        [
            TextValueNeedsFurigana('今日', True),
        ],
        [
            FuriganaValue('今日', 'きょう'),
        ],
        '{今日,きょう}'
    ],
    # single kanji with hirigana, all matched
    [
        [
            TextValueNeedsFurigana('楽', True),
            TextValueNeedsFurigana('し', False),
            TextValueNeedsFurigana('い', False),
        ],
        [
            FuriganaValue('楽', 'たの'),
            FuriganaValue(None, 'し'),
            FuriganaValue(None, 'い'),
        ],
        '{楽,たの}しい',
    ],
    # hirigana first
    [
        [
            TextValueNeedsFurigana('ご', False),
            TextValueNeedsFurigana('飯', True),
        ],
        [
            FuriganaValue(None, 'ご'),
            FuriganaValue('飯', 'はん'),
        ],
        'ご{飯,はん}',
    ],
    #     # hirigana in middle
    [
        [
            TextValueNeedsFurigana('下', True),
            TextValueNeedsFurigana('の', False),
            TextValueNeedsFurigana('名', True),
            TextValueNeedsFurigana('前', True),
        ],
        [
            FuriganaValue('下', 'した'),
            FuriganaValue(None, 'の'),
            FuriganaValue('名', 'な'),
            FuriganaValue('前', 'まえ'),
        ],
        '{下,した}の{名,な}{前,まえ}',
    ],
]


@pytest.mark.parametrize("kanji,furigana,combined", valid_kanji_furigana_combined)
def test_combineTextAndFurigana_valid(kanji, furigana, combined):
    assert utils.combineTextAndFurigana(kanji, furigana) == combined
