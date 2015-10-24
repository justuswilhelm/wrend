from unittest import TestCase

from ..dom import DocumentNode
from ..layout import Frame

from .fixtures import document


class LayoutTestCase(TestCase):
    def test_empty_body(self):
        b = DocumentNode()
