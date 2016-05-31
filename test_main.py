from unittest import TestCase

from nbspacer import main


class TestMain(TestCase):
    def test_help(self):
        with self.assertRaises(SystemExit) as cm:
            main(['--help'])
        self.assertEquals(cm.exception.code, 0)

        with self.assertRaises(SystemExit) as cm:
            main(['--h'])
        self.assertEquals(cm.exception.code, 0)

        with self.assertRaises(SystemExit) as cm:
            main(['--group', 'cs', '--help'])
        self.assertEquals(cm.exception.code, 0)

        with self.assertRaises(SystemExit) as cm:
            main(['--transducer', 'cs.ksvz', '--help'])
        self.assertEquals(cm.exception.code, 0)
