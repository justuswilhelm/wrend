from unittest import TestCase

from ..lexer import HTMLLexer
from .fixtures import tokens


class HTMLLexerTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
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
        expected = str(tokens)
        self.lexer.feed(test_case)
        self.assertEqual(
            expected,
            str(self.lexer.dump()),
        )
