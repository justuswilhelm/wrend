from unittest import TestCase

from ..dom import DocumentNode
from ..layout import Frame


class LayoutTestCase(TestCase):
    def test_empty_document(self):
        b = DocumentNode()
        f = Frame(b)
        f.reflow()
        self.assertEqual(f.w, f.h, f.x, f.y, 0)
