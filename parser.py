from logging import debug

from .lexer import (
    StartTag,
    Data,
    EndTag,
    Comment,
    Decl,
    Pi,
    EOF,
)
from .dom import (
    ElementNode,
    DocumentNode,
    TextNode,
    CommentNode,
    ProcessingInstructionNode,
    DocumentTypeNode,
)


class Parser:

    SELF_CLOSING_TAGS = [
       'AREA',
       'BASE',
       'BR',
       'COL',
       'COMMAND',
       'EMBED',
       'HR',
       'IMG',
       'INPUT',
       'KEYGEN',
       'LINK',
       'META',
       'PARAM',
       'SOURCE',
       'TRACK',
       'WBR',
    ]
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

        document = DocumentNode()
        while not isinstance(self.current, EOF):
            document.child_nodes.append(self.node())
        return document

    def node(self, parent_node=None):
        if not isinstance(self.current, StartTag):
            return self.self_closing(parent_node=parent_node)

        if self.current.name in self.SELF_CLOSING_TAGS:
            debug("Encountered self-closing <%s>", self.current.name)
            return self.self_closing(parent_node=parent_node)

        debug("Entering <%s>", self.current.name)

        # Store token for later matching
        current_node = ElementNode(self.current.name, self.current.attributes)
        self.match_type(StartTag)
        debug("Creating <%s> Node", current_node)

        # While there are things to match
        while self.current:
            if isinstance(self.current, EndTag):
                debug("<%s> children: %s", current_node,
                      current_node.child_nodes)
                debug("Finished adding children to <%s>", current_node)
                self.match_name(current_node.node_name)
                return current_node

            child = self.node(parent_node=current_node)

            debug('Adding child node %s to %s', child, current_node)
            current_node.child_nodes.append(child)
        raise SyntaxError("Oh no!")

    def self_closing(self, parent_node=None):
        # XXX code smell
        if isinstance(self.current, Data):
            child = TextNode(self.current.data, parent_node=parent_node)
            self.match_type(Data)
        elif isinstance(self.current, Comment):
            child = CommentNode(
                self.current.data,
                parent_node=parent_node,
            )
            self.match_type(Comment)
        elif isinstance(self.current, Pi):
            child = ProcessingInstructionNode(
                self.current.data,
                parent_node=parent_node,
            )
            self.match_type(Pi)
        elif isinstance(self.current, Decl):
            child = DocumentTypeNode(
                 self.current.decl,
                 parent_node=parent_node,
            )
            self.match_type(Decl)
        # self-closing start-tag
        elif isinstance(self.current, StartTag):
            child = ElementNode(
                self.current.name,
                attributes=self.current.attributes,
            )
            self.match_type(StartTag)

        if not child:
            raise SyntaxError("Unknown token {}".format(self.current))

        return child

    def next(self):
        self.current = self.tokens.pop(0)

    def match_name(self, name):
        assert type(self.current) in [StartTag, EndTag], (
            "Expected {} to be StartTag or EndTag".format(self.current))
        assert self.current.name == name, (
            "Expected {}.name to equal {}, got {} instead".format(
                type(self.current), name, self.current.name))
        self.next()

    def match_type(self, token_type):
        assert isinstance(self.current, token_type), (
            "Expected {}, got {} instead".format(token_type, self.current))
        self.next()
