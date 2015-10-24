from ..lexer import (
    StartTag,
    Data,
    EndTag,
    EOF,
)

from ..dom import (
    Node,
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

document = Node('#document', Node.DOCUMENT_NODE, child_nodes=[
    Node('HTML', Node.ELEMENT_NODE, child_nodes=[
        Node('BODY', Node.ELEMENT_NODE, child_nodes=[
            Node('H1', Node.ELEMENT_NODE, child_nodes=[
                Node('#text', Node.TEXT_NODE, node_value='Hello World')
            ]),
        ]),
    ]),
])
