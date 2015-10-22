from logging import debug
from collections import namedtuple
from html.parser import HTMLParser

StartTag = namedtuple('StartTag', ['name', 'attributes'])
Data = namedtuple('Data', ['data'])
EndTag = namedtuple('EndTag', ['name'])
EOF = namedtuple('EOF', [])


class HTMLLexer(HTMLParser):
    tokens = []

    def handle_starttag(self, tag, attrs):
        debug('Opening tag %s, attrs %s', tag, attrs)
        self.tokens.append(StartTag(tag, attrs))

    def handle_endtag(self, tag):
        debug('Closing tag %s', tag)
        self.tokens.append(EndTag(tag))

    def handle_data(self, data):
        debug('Data "%s"', data)
        data = data.strip()
        if data:
            self.tokens.append(Data(data))

    def dump(self):
        return self.tokens + [EOF()]
