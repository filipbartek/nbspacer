# nbspacer

A command line utility that replaces appropriate spaces in a HTML document with instances of the character entity `&nbsp;`.
The main target language is Czech.

## Features

* *HTML-aware*: ignores everything enclosed in angle brackets (namely HTML tags)
* *conservative*: only modifies the necessary characters
* *configurable*: choose the transducers or transducer groups you like

While I have tried my best to make the results of the tool correct and predictable,
I still recommend checking the output by hand as some of the transducers may respond to false positives.

## Limitations

* requires [Python](https://www.python.org/)&nbsp;3.5
* the input and output file encoding is hardcoded to UTF&#8209;8
* does not skip the content of the tag `<pre>`

## Quick start

Call `python3 nbspacer.py --help`.

## Czech translation

To enable the Czech translation, follow these steps:

0. `git submodule update --init`
(pull the Czech translation of the `argparse` module)
0. `./nbspacer-cs-msgfmt.sh`
(compile the Czech translation of `nbspacer` and `argparse`)

To enable the Czech translation at runtime, set the environment variable `LANGUAGE` to the value `cs`.

## Special thanks

Most of the Czech language transducers are inspired by the
[relevant article](http://prirucka.ujc.cas.cz/?id=880)
in [Internet Language Reference Book](http://prirucka.ujc.cas.cz/en)
created by [The Institute of the Czech Language of the Academy of Sciences of the Czech Republic](http://www.ujc.cas.cz/en/).
I would like to thank the authors of the reference book for compiling a clear and reasonable set of guidelines.

## Similar tools

* [Automatic NBSP](https://wordpress.org/plugins/automatic-nbsp/) (HTML, Wordpress plugin)
* [&amp;Nbsp; replacer](http://www.nedivse.cz/doplnovani-pevnych-mezer/) (HTML, web interface)
* [vlna](http://ftp.linux.cz/pub/tex/local/cstug/olsak/vlna/) (LaTeX)
