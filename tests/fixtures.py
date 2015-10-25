from ..lexer import (
    StartTag,
    Data,
    EndTag,
    EOF,
)

from ..parser import Parser

tokens = (
    StartTag('HTML', []),
    Data('\n'),
    StartTag('HEAD', []),
    Data('\n'),
    StartTag('TITLE', []),
    Data('\nHello\n'),
    EndTag('TITLE'),
    Data('\n'),
    EndTag('HEAD'),
    Data('\n'),
    StartTag('BODY', []),
    Data('\nWorld\n'),
    EndTag('BODY'),
    Data('\n'),
    EndTag('HTML'),
    EOF(),
)


document = Parser(tokens).parse()
