import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_single_child(self):
        node = ParentNode("p", [LeafNode(None, "Normal Text")])

        html = node.to_html()

        self.assertEqual(html, "<p>Normal Text</p>")

    def test_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Normal text"),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
            ],
        )

        html = node.to_html()

        self.assertEqual(
            html, "<p>Normal text<b>Bold text</b>Normal text<i>Italic text</i></p>"
        )

    def test_multiple_levels(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "First item"),
                        LeafNode("li", "Second item"),
                        LeafNode("li", "Third item"),
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is the "),
                        LeafNode("b", "most important"),
                        LeafNode(None, " paragraph there is"),
                    ],
                ),
            ],
        )

        html = node.to_html()

        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul><p>This is the <b>most important</b> paragraph there is</p></div>",
        )
