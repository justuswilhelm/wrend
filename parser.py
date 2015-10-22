"""
Keep in mind, for future reference, self-closing tags
http://xahlee.info/js/html5_non-closing_tag.html
"""
from collections import namedtuple
from logging import debug

from .lexer import (
    StartTag,
    Data,
    EndTag,
)

Node = namedtuple('Node', ['name', 'nodes'])


class Parser:

    tokens = []
    current = None

    def __init__(self, tokens):
        self.tokens = tokens
        self.next()

    def parse(self):
        while isinstance(self.current, Data):
            self.next()
            debug('Dropping empty start token %s', self.tokens[0])
        debug('Starting recursive descent')

        return self.tag()

    def tag(self):
        start_token = self.current
        self.match_type(StartTag)
        debug(
            "Starting tag: %s", start_token.name)

        nodes = []
        while True:
            if isinstance(self.current, StartTag):
                debug("Entering %s", self.current)
                nodes.append(self.tag())
            elif isinstance(self.current, EndTag):
                self.match_name(start_token.name)
                return Node(start_token.name, nodes)
            else:
                debug("Reading data tag %s", self.current)
                nodes.append(self.current)
                self.match_type(Data)

    def next(self):
        self.current = self.tokens.pop(0)
        debug("Read next token: %s", self.current)

    def match_name(self, name):
        debug("Matching name %s", name)
        assert type(self.current) in [StartTag, EndTag], (
            "Expected {} to be StartTag or EndTag".format(self.current))
        assert self.current.name == name, (
            "Expected {}.name to equal {}, got {} instead".format(
                type(self.current), name, self.current.name))
        self.next()

    def match_type(self, token_type):
        debug("Matching token type %s", token_type)
        assert isinstance(self.current, token_type), (
            "Expected {}, got {} instead".format(token_type, self.current))
        self.next()
