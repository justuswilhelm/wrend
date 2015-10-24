from logging import basicConfig
from sys import argv
from os import getenv

from .lexer import HTMLLexer
from .parser import Parser
from .layout import Frame

basicConfig(level=getenv('LOG_LEVEL'))


def main():
    filename = argv[1]
    lexer = HTMLLexer()

    with open(filename) as fd:
        lexer.feed(fd.read())

    tokens = lexer.dump()
    parser = Parser(tokens)
    dom = parser.parse()
    layout = Frame(dom.child_nodes[2].child_nodes[1])  # body
    layout.reflow(200, 200)
    layout.pprint()
    layout.draw()
