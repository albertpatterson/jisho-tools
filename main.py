# from main import phrase

# # phraseWithFurigana = phrase.getFurigana('スミス： 田中先生は、新しい先生ですか？')
# # phraseWithFurigana = phrase.getFurigana('それは、もう知っているよ。')
# # phraseWithFurigana = phrase.getFurigana('リー：　一年生だから、住む所を選ぶのが一番遅い。')
# # phraseWithFurigana = phrase.getFurigana('ジョン： そう！そして、田中先生が私達の先生になる。')
# # phraseWithFurigana = phrase.getFurigana('あなたの言い訳は聞きたくありません。')
# phraseWithFurigana = phrase.getFurigana(
#     '父： こき使うって、お前、学校で日本語の勉強を始めたら、妙なことを言うようになったな。他の生徒から変な日本語を習っていないだろうか？')

# print(phraseWithFurigana)


from main import term
import json

# word = 'よく'
# # word = 'もどる'
word = 'たべる'
# # word = 'いい'
# word = 'だいじょぶ'
# # word = ' がっく'
# # word = 'ひと'
# word = '食べる'
# word = '金'
# word = '七'
# word = '元気'
# word = '土曜日'
# word = '真面目'
# word = '青春'
# word = 'ぴたりと'

(definitions, anyFailed) = term.getDefinitions(word)
print('\nword: ', word)
print('\nany definitions failed: ', anyFailed)
for definition in definitions:
    print('\ndefinition\n')
    print('kanji', definition.kanji)
    print('furigana', definition.furigana)
    print('definition', definition.definition)
    print('json', str(definition))
    jsonParsed = json.loads(str(definition))
    print('json parsed', jsonParsed)
    print('json parsed kanji', jsonParsed['kanji'])
    print('json parsed furigana', jsonParsed['furigana'])
    print('json parsed definition', jsonParsed['definition'])
