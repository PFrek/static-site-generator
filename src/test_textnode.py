import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextNode.type_bold)
        node2 = TextNode("This is a text node", TextNode.type_bold)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextNode.type_bold)
        node2 = TextNode("This is a different text node", TextNode.type_bold)
        self.assertNotEqual(node, node2)

    def test_neq_text_type(self):
        node = TextNode("This is a text node", TextNode.type_italic)
        node2 = TextNode("This is a text node", TextNode.type_bold)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode(
            "This is a text node", TextNode.type_bold, "http://localhost:80"
        )
        node2 = TextNode(
            "This is a text node", TextNode.type_bold, "http://localhost:999"
        )
        self.assertNotEqual(node, node2)

    def test_default_url(self):
        node = TextNode("This is a text node", TextNode.type_bold)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode(
            "This is a text node", TextNode.type_bold, "http://localhost:8080"
        )
        expected = f"TextNode({node.text}, {node.text_type}, {node.url})"
        self.assertEqual(node.__repr__(), expected)

    def test_split_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextNode.type_text)
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(
            new_nodes[0], TextNode("This is text with a ", TextNode.type_text)
        )
        self.assertEqual(new_nodes[1], TextNode("code block", "code"))
        self.assertEqual(new_nodes[2], TextNode(" word", TextNode.type_text))

    def test_split_bold_and_italic(self):
        node = TextNode(
            "**bold text** and *italic* all mixed together", TextNode.type_text
        )
        split_bold = split_nodes_delimiter([node], "**", TextNode.type_bold)
        new_nodes = split_nodes_delimiter(split_bold, "*", TextNode.type_italic)

        self.assertEqual(new_nodes[0], TextNode("bold text", TextNode.type_bold))
        self.assertEqual(new_nodes[1], TextNode(" and ", TextNode.type_text))
        self.assertEqual(new_nodes[2], TextNode("italic", TextNode.type_italic))
        self.assertEqual(
            new_nodes[3], TextNode(" all mixed together", TextNode.type_text)
        )

    def test_split_no_delimiter_found(self):
        node = TextNode("There is no delimiter here", TextNode.type_text)

        new_nodes = split_nodes_delimiter([node], "*", TextNode.type_italic)

        self.assertEqual(new_nodes, [node])

    def test_split_image(self):
        node = TextNode("Image of a fox", "image", "http://www.animalimages/fox.png")

        new_nodes = split_nodes_delimiter([node], "**", TextNode.type_bold)

        self.assertEqual(new_nodes, [node])

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)

        self.assertEqual(
            extracted[0],
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        )

        self.assertEqual(
            extracted[1],
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted = extract_markdown_links(text)

        self.assertEqual(extracted[0], ("link", "https://www.example.com"))

        self.assertEqual(extracted[1], ("another", "https://www.example.com/another"))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNode.type_text,
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextNode.type_text),
                TextNode(
                    "image",
                    TextNode.type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextNode.type_text),
                TextNode(
                    "second image",
                    TextNode.type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_no_image(self):
        node = TextNode("This text has no image", TextNode.type_text)
        new_nodes = split_nodes_image([node])

        self.assertEqual(new_nodes, [node])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextNode.type_text,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextNode.type_text),
                TextNode(
                    "link",
                    TextNode.type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextNode.type_text),
                TextNode(
                    "second link",
                    TextNode.type_link,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
            ],
        )

    def test_split_no_link(self):
        node = TextNode("This text has no links", TextNode.type_text)
        new_nodes = split_nodes_link([node])

        self.assertEqual(new_nodes, [node])

    def test_text_to_textnodes(self):
        string = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        nodes = text_to_textnodes(string)

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextNode.type_text),
                TextNode("text", TextNode.type_bold),
                TextNode(" with an ", TextNode.type_text),
                TextNode("italic", TextNode.type_italic),
                TextNode(" word and a ", TextNode.type_text),
                TextNode("code block", TextNode.type_code),
                TextNode(" and an ", TextNode.type_text),
                TextNode(
                    "image",
                    TextNode.type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", TextNode.type_text),
                TextNode("link", TextNode.type_link, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
