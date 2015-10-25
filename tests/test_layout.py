from unittest import TestCase

from ..dom import (
    DocumentNode,
    ElementNode,
    TextNode,
)
from ..layout import Frame


class LayoutTestCase(TestCase):
    container_width = 800
    container_height = 600

    def test_empty_document(self):
        d = DocumentNode()
        d_f = Frame(d)
        d_f.reflow()
        self.assertEqual(d_f.w, 0)
        self.assertEqual(d_f.h, 0)

    def test_empty_body(self):
        d = DocumentNode()
        b = ElementNode('BODY')
        d.child_nodes.append(b)
        d_f = Frame(d)
        d_b = d_f.child_frames[0]
        d_f.reflow()
        self.assertEqual(d_f.w, 0)
        self.assertEqual(d_f.h, 0)
        self.assertEqual(d_b.w, 0)
        self.assertEqual(d_b.h, 0)

    def test_text_node_has_size(self):
        t = TextNode("Hello World")
        f = Frame(t)
        f.reflow()
        self.assertGreater(f.w, 0)
        self.assertGreater(f.h, 0)
        self.assertEqual(f.x, 0)
        self.assertEqual(f.y, 0)

    def test_h1_text_nodes_get_displayed_inline(self):
        d = ElementNode('H1')
        t1 = TextNode('Hello world')
        t2 = TextNode('Hello world')
        d.child_nodes.append(t1)
        d.child_nodes.append(t2)
        d_f = Frame(d)
        d_t1 = d_f.child_frames[0]
        d_t2 = d_f.child_frames[1]
        d_f.reflow()

        self.assertEqual(d_f.x, 0)
        self.assertEqual(d_f.y, 0, "Text node must be at y=0")

        self.assertEqual(d_t1.x, 0)
        self.assertEqual(d_t1.y, 0)

        self.assertGreater(d_t2.x, d_t1.x)
        self.assertEqual(d_t2.y, d_t1.y)

        self.assertGreater(d_t1.h, 0)
        self.assertEqual(d_t1.h, d_t2.h)
        self.assertEqual(d_f.h, d_t2.h)
