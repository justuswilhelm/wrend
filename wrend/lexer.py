from logging import debug
from collections import namedtuple
from html.parser import HTMLParser

StartTag = namedtuple('StartTag', ['name', 'attributes'])
Data = namedtuple('Data', ['data'])
EndTag = namedtuple('EndTag', ['name'])
Comment = namedtuple('Comment', ['data'])
Decl = namedtuple('Decl', ['decl'])
Pi = namedtuple('Pi', ['data'])
EOF = namedtuple('EOF', [])


class HTMLLexer(HTMLParser):

    MULTIPLE_WHITESPACE_RE = r'\s+'

    tokens = []

    def __init__(self):
        super().__init__(convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        tag = tag.upper()
        debug('Opening tag %s, attrs %s', tag, attrs)
        self.tokens.append(StartTag(tag, attrs))

    def handle_endtag(self, tag):
        tag = tag.upper()
        debug('Closing tag %s', tag)
        self.tokens.append(EndTag(tag))

    def handle_data(self, data):
        debug('Data "%s"', data)
        if data:
            self.tokens.append(Data(data))

    def handle_comment(self, data):
        debug('Comment "%s"', data)
        if data:
            self.tokens.append(Comment(data))

    def handle_decl(self, decl):
        debug('Decl %s', decl)
        self.tokens.append(Decl(decl))

    def handle_pi(self, data):
        debug('Pi %s', data)
        self.tokens.append(Pi(data))

    def dump(self):
        return tuple(self.tokens + [EOF()])
