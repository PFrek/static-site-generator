import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_render_no_tag(self):
        node = LeafNode(None, "Hello I have no tag")
        html = node.to_html()

        self.assertEqual(html, "Hello I have no tag")

    def test_render_tag_no_props(self):
        node = LeafNode("p", "Hello I have no props")
        html = node.to_html()

        self.assertEqual(html, "<p>Hello I have no props</p>")

    def test_render_tag_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html = node.to_html()

        self.assertEqual(html, '<a href="https://www.google.com">Click me!</a>')

    def test_no_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()
