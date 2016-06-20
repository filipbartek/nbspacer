import json
from argparse import Namespace
from io import StringIO
from itertools import zip_longest
from unittest import TestCase, skip

import cs
import en
import transducer
from transducer import Transducer

assert cs
assert en


class TestMasterTransducer(TestCase):
    @staticmethod
    def configure_master(transducers=[], groups=[]):
        namespace = Namespace()
        setattr(namespace, 'help', False)
        setattr(namespace, 'group', groups)
        setattr(namespace, 'transducer', transducers)
        transducer.master.configure(namespace)

    @staticmethod
    def transduce(transducer, string):
        assert isinstance(transducer, Transducer)
        infile = StringIO(string)
        outfile = StringIO()
        transducer.process_file(infile, outfile)
        outfile.seek(0)
        return outfile.getvalue()

    def transduce_assert(self, t, cases):
        assert isinstance(t, Transducer)
        for input, expected in cases:
            actual = self.transduce(t, input)
            self.assertEqual(expected, actual)

    def test_cs(self):
        self.configure_master(groups=[['cs']])
        cases = json.load(open('test_masterTransducer_cs.json'))
        self.transduce_assert(transducer.master, cases)

    def test_cs_group(self):
        cases = json.load(open('test_masterTransducer_cs.json'))
        self.transduce_assert(cs.lang_cs, cases)

    @skip('This test is too strict.')
    def test_prirucka(self):
        self.configure_master()
        infile = open('test/prirucka-nonbsp.html')
        outfile = StringIO()
        transducer.master.process_file(infile, outfile)
        outfile.seek(0)
        expected = open('test/prirucka-orig.html')
        for (i, (a, e)) in enumerate(zip_longest(outfile, expected)):
            self.assertEqual(a, e, 'Line number: {0}'.format(i + 1))
