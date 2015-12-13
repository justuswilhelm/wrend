from unittest import TestCase

from ..dom import TextNode


class TextNodeTestCase(TestCase):
    def test_whole_text(self):
        t = TextNode("\r\r\n\n hello world  yo\n")
        self.assertEqual(
            t.whole_text, " hello world yo ")
