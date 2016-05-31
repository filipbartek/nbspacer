"""
This package several defines `Transducer` classes. The instances of `Transducer` can be used to transduce a HTML file
using the method `process_file`.
"""

import gettext
import heapq
import itertools
import re
import sys
from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser
from collections import OrderedDict
from enum import Enum
from itertools import chain
from queue import PriorityQueue

from ordered_set import OrderedSet
from overrides import overrides

import config

_ = gettext.translation(config.domain, localedir=config.localedir, fallback=True).gettext


class Transducer(metaclass=ABCMeta):
    def __init__(self, name=None, description=None, examples=None):
        self.name = name
        self.description = description
        self.examples = examples

    def __str__(self):
        return self.name

    def print_help(self, file=sys.stdout):
        file.write(_('Transducer "{0}":\n').format(self.name))
        if self.description:
            file.write(_('  Description: {0}\n').format(self.description))
        if self.examples:
            file.write(_('  Examples:\n'))
            for before in self.examples:
                # Before:
                file.write('    -{0}\n'.format(before))
                # After:
                file.write('    +{0}\n'.format(self.transduce_html(before)))

    @abstractmethod
    def substitute(self, string, indices):
        """
        Translates a string.
        :return: a pair of string and indices
        """
        raise NotImplementedError()

    def transduce_html(self, html):
        # Load html
        inside_tag = False
        content_list = []
        tags = OrderedDict()
        i = 0
        tag = []
        for c in html:
            assert isinstance(c, str)
            assert len(c) == 1
            if c == r'<':
                inside_tag = True
                tag.append(c)
                continue
            if c == r'>':
                inside_tag = False
                tag.append(c)
                continue
            if inside_tag:
                tag.append(c)
                continue
            if tag:
                tags[i] = ''.join(tag)
                tag = []
            content_list.append(c)
            i += 1
        content = ''.join(content_list)
        # Transduce
        content_transduced, indices = self.substitute(content, range(len(content)))
        transduced = zip(indices, content_transduced)
        # Insert tags
        # The `key` argument requires Python 3.5
        merged = heapq.merge(tags.items(), transduced, key=lambda x: x[0])
        return ''.join((string for i, string in merged))

    def process_file(self, infile, outfile):
        outfile.write(self.transduce_html(infile.read()))


class ReTransducer(Transducer):
    class Align(Enum):
        left = 'left'
        right = 'right'

    def __init__(self, pattern, replacement, align=Align.left, fixpoint=True, name=None, description=None,
                 examples=None):
        super().__init__(name=name, description=description, examples=examples)
        self.pattern = pattern
        assert isinstance(replacement, dict)
        self.replacement = replacement
        self.align = align
        self.fixpoint = fixpoint

    @overrides
    def print_help(self, file=sys.stdout):
        super().print_help(file)
        file.write(_('  Pattern: {0}\n').format(self.pattern))
        file.write(_('  Replacement: {0}\n').format(self.replacement))
        file.write(_('  Align: {0}\n').format(self.align))
        file.write(_('  Fixpoint: {0}\n').format(self.fixpoint))

    @overrides
    def substitute(self, string, indices):
        result_string, indices = self.substitute_once(string, indices)
        if self.fixpoint:
            while result_string != string:
                string = result_string
                result_string, indices = self.substitute_once(string, indices)
        return result_string, indices

    def substitute_once(self, string, indices):
        assert isinstance(string, str)
        indices = list(indices)
        assert len(string) == len(indices)
        n = len(string)
        i = 0
        result_string = []
        result_indices = []
        match = re.search(self.pattern, string)
        if match:
            q = PriorityQueue()
            for key, value in self.replacement.items():
                span = match.span(key)
                assert span
                q.put((span, value))
            while not q.empty():
                (start, end), value = q.get()
                assert start >= i
                assert start < len(string)
                # TODO: Allow align to be set in value
                align = self.align
                result_string.append(string[i:start])
                result_indices.append(indices[i:start])
                i = start
                if align == self.Align.left:
                    pretend = indices[start]
                else:
                    pretend = indices[end - 1]
                result_string.append(value)
                result_indices.append([pretend] * len(value))
                i = end
        result_string.append(string[i:n])
        result_indices.append(indices[i:n])
        return ''.join(result_string), itertools.chain.from_iterable(result_indices)


class WordsNbspSubstituter(ReTransducer):
    def __init__(self, words, name=None, description=None, examples=None):
        words = list(words)
        pattern = '( )'.join(words)
        replacement = {i: r'&nbsp;' for i in range(1, len(words))}
        super().__init__(pattern, replacement, name=name, description=description, examples=examples)


class DottedNbspSubstituter(WordsNbspSubstituter):
    @overrides
    def __init__(self, words, name=None, description=None, examples=None):
        words_iter = iter(words)
        head_word_dotted = r'\b{0}\.'.format(next(words_iter))
        tail_words_dotted = (r'{0}\.'.format(word) for word in words_iter)
        words_dotted = chain([head_word_dotted], tail_words_dotted)
        super().__init__(words_dotted, name=name, description=description, examples=examples)


class TransducerGroup(Transducer):
    def __init__(self, name, description=None):
        super().__init__(name=name, description=description)
        self.transducers = []

    def add(self, transducer):
        self.transducers.append(transducer)

    def help(self):
        transducer_names = ', '.join((transducer.name for transducer in self.transducers))
        if self.description:
            return '{0}: {1}'.format(self.description, transducer_names)
        return transducer_names

    @overrides
    def print_help(self, file=sys.stdout):
        file.write(_('Transducer group "{0}":\n').format(self.name))
        if self.description:
            file.write(_('  Description: {0}\n').format(self.description))
        file.write(_('  Transducers:\n    {0}').format('\n    '.join(map(str, self.transducers))))
        file.write('\n')

    @overrides
    def substitute(self, string, indices):
        for transducer in self.transducers:
            string, indices = transducer.substitute(string, indices)
        return string, indices


class MasterTransducer(Transducer):
    def __init__(self):
        super().__init__([])
        self.transducers = OrderedDict()
        self.groups = OrderedDict()
        self.selected = OrderedSet()
        self.parser = None

    def add(self, transducer, groups=None):
        """
        The transducers are guaranteed to execute in the order in which they are added.
        """
        assert isinstance(transducer, Transducer)
        name = transducer.name
        assert name is not None
        assert name not in self.transducers.keys(), 'Duplicit transducer "{0}"'.format(name)
        self.transducers[name] = transducer
        for group in groups:
            assert group in self.groups.values()
            group.add(transducer)

    def add_group(self, name, description=None):
        assert name not in self.groups.keys(), 'Duplicit group "{0}"'.format(name)
        group = TransducerGroup(name, description)
        self.groups[name] = group
        return group

    def add_arguments(self, parser):
        assert isinstance(parser, ArgumentParser)
        self.parser = parser
        group_names = list(self.groups.keys())
        parser.add_argument('--group', '-g', nargs='+', action='append', choices=group_names, metavar='G',
                            help=_(
                                'Enables the transducer group G. Combine with --help to show detailed information. Available groups: {0}').format(
                                ', '.join(group_names)))
        transducer_names = list(self.transducers.keys())
        parser.add_argument('--transducer', '-t', nargs='+', action='append', choices=transducer_names, metavar='T',
                            help=_(
                                'Enables the transducer T. Combine with --help to show detailed information. Available transducers: {0}').format(
                                ', '.join(transducer_names)))

    def configure(self, args, file=sys.stdout):
        self.selected.clear()
        if args.group:
            for group_name in chain.from_iterable(args.group):
                group = self.groups[group_name]
                if args.help:
                    self.parser.print_help(file)
                    file.write('\n')
                    group.print_help(file)
                    self.parser.exit()
                for transducer in group.transducers:
                    self.selected.add(transducer)
        if args.transducer:
            for transducer_name in chain.from_iterable(args.transducer):
                transducer = self.transducers[transducer_name]
                if args.help:
                    self.parser.print_help(file)
                    file.write('\n')
                    transducer.print_help(file)
                    self.parser.exit()
                self.selected.add(transducer)
        if len(self.selected) == 0:
            # If no transducer is selected explicitly, all transducers are used.
            self.selected = self.transducers.values()

    @overrides
    def substitute(self, string, indices):
        for transducer in self.selected:
            string, indices = transducer.substitute(string, indices)
        return string, indices


master = MasterTransducer()
