from unittest import TestCase

from ..lexer import (
    HTMLLexer,
    StartTag,
    Data,
    EndTag,
    Comment,
    EOF,
)


class HTMLLexerTestCase(TestCase):
    def setUp(self):
        self.lexer = HTMLLexer()

    def test_simple_case(self):
        test_case = """\
<html>
<head>
<title>
Hello
</title>
</head>
<body>
World
</body>
</html>
"""
        expected = str([
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
        ])
        self.lexer.feed(test_case)
        self.assertEqual(
            str(self.lexer.dump()),
            expected,
        )
