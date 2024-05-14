import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.google.com", "alt": "Link to google website"},
        )

        html = node.props_to_html()

        self.assertEqual(
            html, ' href="https://www.google.com" alt="Link to google website"'
        )
