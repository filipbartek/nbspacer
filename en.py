import gettext

from transducer import master, WordsNbspSubstituter

t = gettext.translation('nbspacer', localedir='locale', fallback=True)
_ = t.gettext

# Groups:
lang_en = master.add_group('en', _('English language'))
punctuation = master.add_group('punctuation')
ellipsis = master.add_group('ellipsis')

# http://www.chicagomanualofstyle.org/qanda/data/faq/topics/SpecialCharacters/faq0003.html
# http://practicaltypography.com/ellipses.html

# Transducers:

ellipsis_periods_after_period = WordsNbspSubstituter([r'\. \.'] + [r'\.'] * 2, 'ellipsis_periods_after_period')
ellipsis_periods_after_period.examples = ['I am fine. . . . And you?']
master.add(ellipsis_periods_after_period, [lang_en, punctuation, ellipsis])

ellipsis_periods_after_word = WordsNbspSubstituter([r'\w'] + [r'\.'] * 3, 'ellipsis_periods_after_word')
ellipsis_periods_after_word.examples = ['And so on . . .']
master.add(ellipsis_periods_after_word, [lang_en, punctuation, ellipsis])

ellipsis_periods = WordsNbspSubstituter([r'\.'] * 3, 'ellipsis_periods')
ellipsis_periods.examples = ['1, 2, 3, . . .']
master.add(ellipsis_periods, [lang_en, punctuation, ellipsis])

ellipsis_special = WordsNbspSubstituter([r'\w', r'(?:…|&hellip;)'], 'ellipsis_special')
ellipsis_special.examples = ['And so on …', 'And so on &hellip;']
master.add(ellipsis_special, [lang_en, punctuation, ellipsis])
