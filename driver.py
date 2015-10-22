from logging import basicConfig
from sys import argv
from os import getenv

from .lexer import HTMLLexer
from .parser import Parser
from .pprint import pprint

basicConfig(level=getenv('LOG_LEVEL'))


def main():
    filename = argv[1]
    lexer = HTMLLexer()

    with open(filename) as fd:
        lexer.feed(fd.read())

    tokens = lexer.dump()
    parser = Parser(tokens)
    pprint(parser.parse())
