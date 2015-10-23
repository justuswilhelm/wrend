from unittest import TestCase

from ..parser import Parser
from .fixtures import tokens


class ParserTestCase(TestCase):
    def setUp(self):
        self.parser = Parser(tokens)

    def test_it_parses_yay(self):
        self.parser.parse()
