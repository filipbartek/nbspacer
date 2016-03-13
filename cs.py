import gettext

import config
from transducer import WordsNbspSubstituter, DottedNbspSubstituter, ReTransducer, master

_ = gettext.translation(config.domain, localedir=config.localedir, fallback=True).gettext

# http://prirucka.ujc.cas.cz/?id=880

# Missing:
# mezi číslem a názvem počítaného jevu, např. 500 lidí, 365 dní, 10 kilogramů, strana 2, tabulka 3, 5. pluk, 8. kapitola, II. patro, Karel IV.
# ve složených zkratkách, v ustálených spojeních a v různých kódech, např. [...] PS PČR, FF UK
# mezi zkratkami rodných jmen a příjmeními, např. Fr. Daneš, M. Těšitelová

# Groups:
lang_cs = master.add_group('cs', _('Czech language'))
prirucka = master.add_group('prirucka', 'Internetová jazyková příručka')
preposition = master.add_group('preposition', _('prepositions'))
conjunction = master.add_group('conjunction', _('conjunctions'))
number = master.add_group('number', _('numbers'))
unit = master.add_group('unit', _('units'))
abbreviation = master.add_group('abbreviation', _('abbreviations'))
acronym = master.add_group('acronym', _('acronyms'))
vlna = master.add_group('vlna', _('Inspired by the LaTeX package vlna'))

# Transducers:

master.add(WordsNbspSubstituter([r'\b[ksvzKSVZ]', r'\w'], 'cs.ksvz',
                                description=_('Non-syllabic preposition and the following word'),
                                examples=['k mostu', 's bratrem', 'v Plzni', 'z nádraží']),
           [lang_cs, prirucka, preposition, vlna])

ou = WordsNbspSubstituter([r'\b[ouOU]', r'\w'], 'cs.ou')
ou.description = _('One-letter syllabic preposition and the following word')
ou.examples = ['u babičky', 'o páté']
master.add(ou, [lang_cs, prirucka, preposition])

ai = WordsNbspSubstituter([r'\b[aiAI]', r'\w'], 'cs.ai')
ai.description = _('One-letter conjunction and the following word')
ai.examples = ['máma a táta', 'I já jsem tam byl.']
master.add(ai, [lang_cs, prirucka, conjunction])

master.add(WordsNbspSubstituter([r'\b\d{1,3}', r'\d{3}\b'], 'thousands_separator',
                                description=_('Thousands separator'),
                                examples=['2 500', '1 000 000']),
           [lang_cs, prirucka, number])

master.add(WordsNbspSubstituter([r'\d', r'%'], 'number_percent',
                                examples=['50 %']),
           [lang_cs, prirucka, number, unit])

master.add(WordsNbspSubstituter([r'[§#*©]', r'\d'], 'special_number',
                                description=_('Special character followed by a number'),
                                examples=['§ 23', '# 26', '* 1921', '© 2008']),
           [lang_cs, prirucka, number])  # [§#*†]
# TODO: Support more special characters

strana = master.add_group('cs.strana', _('Variations of the word "strana"'))
master.add(WordsNbspSubstituter([r'\b[sS]trana', r'\d'], 'cs.strana', examples=['strana 53']),
           [lang_cs, prirucka, number, strana])
master.add(WordsNbspSubstituter([r'\b[sS]tr\.', r'\d'], 'cs.strana.str', examples=['str. 53']),
           [lang_cs, prirucka, number, abbreviation, strana])
master.add(WordsNbspSubstituter([r'\b[sS]\.', r'\d'], 'cs.strana.s', examples=['s. 53']),
           [lang_cs, prirucka, number, abbreviation, strana])

cislo = master.add_group('cs.cislo', _('Variations of the word "číslo'))
master.add(WordsNbspSubstituter([r'\b[čČ]íslo', r'\d'], 'cs.cislo', examples=['číslo 9']),
           [lang_cs, prirucka, number, cislo])
master.add(WordsNbspSubstituter([r'\b[čČ]\.', r'\d'], 'cs.cislo.c', examples=['č. 9']),
           [lang_cs, prirucka, number, abbreviation, cislo])

# master.add(WordsNbspSubstituter([r'\bobr\.', r'\d']))
# master.add(WordsNbspSubstituter([r'\btab\.', r'\d']))

si_unit_prefixes = ['T', 'G', 'M', 'k', 'h', 'da', 'd', 'c', 'm', 'μ', 'n', 'p']
si_unit_bases = ['m', 'g', 's', 'A', 'K', 'mol', 'cd']
si_unit_post = r'(?:{0})?(?:{1})\b'.format('|'.join(si_unit_prefixes), '|'.join(si_unit_bases))
master.add(WordsNbspSubstituter([r'\d', si_unit_post], 'si',
                                description=_('Number and a unit of the International System of Units (SI)'),
                                examples=['10 kg', '1 damol']),
           [lang_cs, prirucka, number, abbreviation, unit])
# TODO: Add more units, for example m², B, b

currencies = [r'Kč\b', '€']
master.add(WordsNbspSubstituter([r'\d', r'(?:{0})'.format('|'.join(currencies))], 'cs.currency',
                                description=_('Number and a currency'),
                                examples=['1 Kč', '250 €']),
           [lang_cs, prirucka, number, abbreviation, unit])

# TODO: Only accept valid dates
master.add(WordsNbspSubstituter([r'\b\d?\d\.', r'\d?\d\.'], 'cs.date',
                                description=_('Czech date'),
                                examples=['21. 6.']),
           [lang_cs, prirucka, number])

master.add(WordsNbspSubstituter([r'\d', r'(?:h(?:od)?|min)\.?\b'], 'cs.time',
                                description=_('Number and a Czech time unit'),
                                examples=['8 hod.', 'Zbývá 5 min do konce zápasu.']),
           [lang_cs, prirucka, number, abbreviation, unit])

master.add(WordsNbspSubstituter([r'\d', r'°C\b'], 'deg_celsius',
                                description=_('Number of degrees Celsius'),
                                examples=['19 °C']),
           [lang_cs, prirucka, number, abbreviation, unit])

master.add(WordsNbspSubstituter([r'\d', r':', r'\d'], 'ratio',
                                description=_('Ratio'),
                                examples=['1 : 50 000', '5 : 3']),
           [lang_cs, prirucka, number])

# Acronyms:

master.add(DottedNbspSubstituter(['a', 's'], 'cs.acronym.as',
                                 description='The acronym of "akciová společnost"',
                                 examples=['a. s.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['s', 'r', 'o'], 'cs.acronym.sro',
                                 description='The acronym of "společnost s ručením omezeným"',
                                 examples=['s. r. o.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['v', 'v', 'i'], 'cs.acronym.vvi',
                                 description='The acronym of "veřejná výzkumná instituce"',
                                 examples=['v. v. i.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['[Rr]', 'č'], 'cs.acronym.rc',
                                 description='The acronym of "rodné číslo"',
                                 examples=['r. č.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['(?:[jJ]|[mM]n)', 'č'], 'cs.acronym.jmnc',
                                 description='The acronym of "jednotné číslo" and "množné číslo"',
                                 examples=['j. č.', 'mn. č.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['př', 'n', 'l'], 'cs.acronym.prnl',
                                 description='The acronym of "před naším letopočtem"',
                                 examples=['2016 př. n. l.']),
           [lang_cs, prirucka, abbreviation, acronym])
master.add(DottedNbspSubstituter(['n', 'l'], 'cs.acronym.nl',
                                 description='The acronym of "našeho letopočtu"',
                                 examples=['2016 n. l.']),
           [lang_cs, prirucka, abbreviation, acronym])

master.add(ReTransducer(r'\bČSN( )\d{2}( |&nbsp;)\d{4}\b', {1: r'&nbsp;', 2: r'&nbsp;'}, name='cs.csn',
                        examples=['ČSN 01 6910']),
           [lang_cs, prirucka, abbreviation, acronym])

master.add(WordsNbspSubstituter([r'\b(?:[Tt]j|[Tt]zv|[Tt]zn|[Nn]apř)\.', r'\w'], 'cs.acronym.tj_tzv_tzn_napr',
                                description='The acronym of "to je", "takzvaný", "to znamená" or "například" followed by a word',
                                examples=['tj. člověk', 'tzv. člověk', 'tzn. člověk', 'např. člověk']),
           [lang_cs, prirucka, abbreviation, acronym])

master.add(WordsNbspSubstituter([r'\b(?:[Pp]|[Mm]jr|[Ii]ng|[Bb]c|[Mm]gr)\.', r'\w'], 'cs.acronym.title',
                                description='The acronym of the title "pan", "major", "inženýr", "bakalář" or "magistr" followed by a word',
                                examples=['p. Kim', 'Mjr. Kim', 'Ing. Kim', 'Bc. Kim', 'Mgr. Kim']),
           [lang_cs, prirucka, abbreviation, acronym])
# TODO: Add more titles
