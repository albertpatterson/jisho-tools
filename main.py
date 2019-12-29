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

# word = 'よく'
# # word = 'もどる'
# # word = 'たべる'
# # word = 'いい'
# word = 'だいじょぶ'
# # word = ' がっく'
# # word = 'ひと'
# word = '食べる'
# word = '金'
# word = '七'
# word = '元気'
# word = '土曜日'
word = '真面目'

(definitions, anyFailed) = term.getDefinitions(word)
print('\nword: ', word)
print('\nany definitions failed: ', anyFailed)
for definition in definitions:
    print('\ndefinition\n')
    print(definition)
    print()
