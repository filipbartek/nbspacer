#!/bin/bash

mkdir -p locale/cs/LC_MESSAGES
msgfmt nbspacer-cs.po -o locale/cs/LC_MESSAGES/nbspacer.mo
msgfmt argparse-cs/argparse-cs.po -o locale/cs/LC_MESSAGES/argparse.mo
