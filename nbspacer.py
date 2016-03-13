#!/usr/bin/python

"""
nbspacer replaces spaces with &nbsp; in a HTML document where appropriate.
Its main target language is Czech.

Sources of inspiration:
* http://prirucka.ujc.cas.cz/?id=880
* http://www.chicagomanualofstyle.org/qanda/data/faq/topics/SpecialCharacters/faq0003.html

Big thanks go to the maintainers of Prirucka for compiling a clear and reasonable set of relevant guidelines.
"""

# TODO: Support command line options:
# user-defined patterns
# gracious treatment of malformed documents

# TODO: Print number of matches by pattern
# TODO: Add interactive mode that asks in dubious cases
# TODO: Enable the user to specify the encoding
# TODO: Add tests
# TODO: Account for <pre></pre>

if __name__ == '__main__':
    import argparse
    import gettext
    import sys

    import cs
    import config
    import en
    import transducer

    # Prevent the cs and en imports from being optimized away
    assert cs
    assert en

    gettext.bindtextdomain('argparse', config.localedir)
    gettext.textdomain('argparse')

    _ = gettext.translation(config.domain, localedir=config.localedir, fallback=True).gettext

    # Initialize the parser
    description = _('Replaces space characters with &nbsp; where appropriate in a HTML document. ' \
                    'The replacement functionality is divided in transducers. ' \
                    'Every transducer takes care of a single type of replacements. ' \
                    'The transducers are grouped into named groups.')
    parser = argparse.ArgumentParser(description=description, add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help=_('show this help message and exit'))
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding='utf_8'), default=sys.stdin, help=_('input file'))
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w', encoding='utf_8'), default=sys.stdout, help=_('ouptut file'))
    # parser.add_argument('--encoding', nargs=1, type=str, default='utf_8')
    transducer.master.add_arguments(parser)

    # Parse the command line arguments
    args = parser.parse_args()
    transducer.master.configure(args)

    if args.help:
        parser.print_help()
        parser.exit()

    transducer.master.process_file(args.infile, args.outfile)
    args.infile.close()
    args.outfile.close()
