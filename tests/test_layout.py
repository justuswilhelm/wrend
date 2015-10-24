from unittest import TestCase

from ..layout import Frame

from .fixtures import document


class LayoutTestCase(TestCase):
    def test_simple_layout(self):
        Frame(document)
