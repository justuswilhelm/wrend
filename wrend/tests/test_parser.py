from unittest import TestCase

from ..parser import Parser
from .fixtures import tokens


class ParserTestCase(TestCase):
    def test_it_parses_yay(self):
        parser = Parser(tokens)
        parser.parse()
