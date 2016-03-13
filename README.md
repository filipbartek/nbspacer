# nbspacer

A command line utility that replaces all the appropriate spaces in a HTML document with instances of `&nbsp;`.
The main target language is Czech.

## Features

* HTML-aware: only touches the content outside the tags delimited by angle brackets
* conservative: only changes the necessary characters
* configurable: choose the transducers or transducer groups you like

While I have tried my best to make the execution of the tool precise and predictable,
I still recommend checking the result manually as some of the transducers may respond to false positives.

## Limitations

* the input and output file encoding is hardcoded to UTF-8
* does not skip the content of the tag `<pre>`
* requires [Python](https://www.python.org/) 3.5

## Quick start

Call `python3 nbspacer.py --help`.

## Czech translation

For the Czech translation to work, you must follow these steps:

0. `git submodule update --init`
0. `./nbspacer-cs-msgfmt.sh`

To enable the Czech translation at runtime, set the environment variable `LANGUAGE` to the value `cs`.

## Special thanks

Most of the Czech language transducers are inspired by the
[corresponding article](http://prirucka.ujc.cas.cz/?id=880)
in [Internet Language Reference Book](http://prirucka.ujc.cas.cz/en)
created by [The Institute of the Czech Language of the Academy of Sciences of the Czech Republic](http://www.ujc.cas.cz/en/).
I would like to thank the authors of the reference book for compiling a clear and reasonable set of guidelines.

## Similar tools

* [Automatic NBSP](https://wordpress.org/plugins/automatic-nbsp/) (HTML, Wordpress plugin)
* [&amp;Nbsp; replacer](http://www.nedivse.cz/doplnovani-pevnych-mezer/) (HTML, web interface)
* [vlna](http://ftp.linux.cz/pub/tex/local/cstug/olsak/vlna/) (LaTeX)
