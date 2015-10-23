from ..lexer import (
    StartTag,
    Data,
    EndTag,
    EOF,
)

tokens = [
    StartTag('HTML', []),
    StartTag('HEAD', []),
    StartTag('TITLE', []),
    Data('Hello'),
    EndTag('TITLE'),
    EndTag('HEAD'),
    StartTag('BODY', []),
    Data('World'),
    EndTag('BODY'),
    EndTag('HTML'),
    EOF(),
]
