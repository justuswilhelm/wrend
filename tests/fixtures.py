from ..lexer import (
    StartTag,
    Data,
    EndTag,
    EOF,
)

from ..dom import (
    DocumentNode,
    TextNode,
    ElementNode,
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

document = DocumentNode(child_nodes=[
    ElementNode('HTML', child_nodes=[
        ElementNode('BODY', child_nodes=[
            ElementNode('H1', child_nodes=[
                TextNode(node_value='Hello World')
            ]),
        ]),
    ]),
])
