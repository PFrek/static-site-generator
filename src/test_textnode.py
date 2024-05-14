import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", "italics")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", "bold", "http://localhost:80")
        node2 = TextNode("This is a text node", "bold", "http://localhost:999")
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", "bold", "http://localhost:8080")
        expected = f"TextNode({node.text}, {node.text_type}, {node.url})"
        self.assertEqual(node.__repr__(), expected)


if __name__ == "__main__":
    unittest.main()
