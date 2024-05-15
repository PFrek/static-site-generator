import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    paragraph_to_html,
    get_quote_contents,
    quote_to_html,
    get_code_contents,
    code_to_html,
    get_heading_contents,
    heading_to_html,
    unordered_to_html,
    ordered_to_html,
)

from htmlnode import ParentNode, LeafNode


class TestBlockMarkdown(unittest.TestCase):
    def test_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_many_blank_lines(self):
        markdown = """This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line


* This is a list
* with items


"""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_single_line(self):
        markdown = "Single line **markdown**"

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, ["Single line **markdown**"])

    def test_empty_markdown(self):
        markdown = ""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, [])

    # Block to block type
    def test_headings(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
            "Not a heading",
            "#Close but not quite",
        ]

        block_types = list(map(block_to_block_type, blocks))

        self.assertEqual(
            block_types,
            [
                BlockType.heading,
                BlockType.heading,
                BlockType.heading,
                BlockType.heading,
                BlockType.heading,
                BlockType.heading,
                BlockType.paragraph,
                BlockType.paragraph,
            ],
        )

    def test_code(self):
        blocks = [
            "```Code in one line```",
            "```\nMultiline code\nreturn 0\n```",
            "```No closing backticks",
            "Only closing backticks?```",
        ]

        block_types = list(map(block_to_block_type, blocks))

        self.assertEqual(
            block_types,
            [
                BlockType.code,
                BlockType.code,
                BlockType.paragraph,
                BlockType.paragraph,
            ],
        )

    def test_quote(self):
        blocks = [
            ">Single line quote",
            "> With a space after the '>'",
            ">Multiline quotes\n>Should be detected too\n> Even if they mix styles",
            "Definitely not a quote",
            ".> Also not a quote",
        ]

        block_types = list(map(block_to_block_type, blocks))

        self.assertEqual(
            block_types,
            [
                BlockType.quote,
                BlockType.quote,
                BlockType.quote,
                BlockType.paragraph,
                BlockType.paragraph,
            ],
        )

    def test_unordered_list(self):
        blocks = [
            "* Star list with one item",
            "- Dash list with one item",
            "* Star\n* list\n* with\n* multiple\n* items",
            "- Dash\n- list\n- with\n- multiple\n- items",
            "*Star missing space",
            "-Dash missing space",
            "* Almost\n* a star\n*list but no space",
            "- Almost\n- a dash\n-list but no space",
        ]

        block_types = list(map(block_to_block_type, blocks))

        self.assertEqual(
            block_types,
            [
                BlockType.unordered_list,
                BlockType.unordered_list,
                BlockType.unordered_list,
                BlockType.unordered_list,
                BlockType.paragraph,
                BlockType.paragraph,
                BlockType.paragraph,
                BlockType.paragraph,
            ],
        )

    def test_ordered_list(self):
        blocks = [
            "1. Ordered list with one item",
            "1. Ordered\n2. list with\n3. many items",
            "1.Missing space",
            "1. Also\n2.missing\n3. space",
            "1 No point\n2 separating index",
            "1. Wrong order\n3. Of indexes",
            "0. Starting\n1. At\n2. zero is not allowed",
        ]

        block_types = list(map(block_to_block_type, blocks))

        self.assertEqual(
            block_types,
            [
                BlockType.ordered_list,
                BlockType.ordered_list,
                BlockType.paragraph,
                BlockType.paragraph,
                BlockType.paragraph,
                BlockType.paragraph,
                BlockType.paragraph,
            ],
        )

    # Block to html
    def test_paragraph_to_html(self):
        paragraphs = [
            "Simple paragraph",
            "Multiline\nParagraph\nshould also work",
        ]
        not_paragraphs = [
            "> Not a paragraph",
            "```Actual code```",
            "1. Ordered\n2. List",
            "* Unordered\n* list",
        ]

        for block in paragraphs:
            html = paragraph_to_html(block)
            self.assertEqual(html, LeafNode("p", block))

        for block in not_paragraphs:
            with self.assertRaises(ValueError):
                html = paragraph_to_html(block)

    def test_quote_to_html(self):
        quotes = [
            "> Single line quote",
            "> Multiline\n> quotes\n> also\n> work",
        ]

        not_quotes = [
            "A paragraph",
            "```Code block```",
            "# Heading",
            "1. List\n2. Not\n3. Quote",
        ]

        for block in quotes:
            html = quote_to_html(block)
            contents = get_quote_contents(block)
            self.assertEqual(html, LeafNode("blockquote", contents))

        for block in not_quotes:
            with self.assertRaises(ValueError):
                html = quote_to_html(block)

    def test_code_to_html(self):
        codes = [
            "```Single line code```",
            "```\nMulti\nline\ncode\nreturn 0\n```",
        ]

        not_codes = [
            "Simple paragraph",
            "```No closing backticks",
        ]

        for block in codes:
            html = code_to_html(block)
            contents = get_code_contents(block)

            self.assertEqual(
                html, ParentNode("pre", None, [LeafNode("code", contents)])
            )

        for block in not_codes:
            with self.assertRaises(ValueError):
                html = code_to_html(block)

    def test_heading_to_html(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]

        not_headings = ["####### Level 7", "Paragraph"]

        for i in range(len(headings)):
            block = headings[i]
            html = heading_to_html(block)

            contents = get_heading_contents(block)

            self.assertEqual(html, LeafNode(f"h{i+1}", contents))

        for block in not_headings:
            with self.assertRaises(ValueError):
                html = heading_to_html(block)

    def test_unordered_to_html(self):
        lists = [
            "* Single item",
            "* more\n* than\n* one\n* item",
            "- single dash",
            "- many\n- dashes\n- here",
        ]

        htmls = list(map(unordered_to_html, lists))

        self.assertEqual(htmls[0], ParentNode("ul", [LeafNode("li", "Single item")]))

        self.assertEqual(
            htmls[1],
            ParentNode(
                "ul",
                [
                    LeafNode("li", "more"),
                    LeafNode("li", "than"),
                    LeafNode("li", "one"),
                    LeafNode("li", "item"),
                ],
            ),
        )

        self.assertEqual(htmls[2], ParentNode("ul", [LeafNode("li", "single dash")]))

        self.assertEqual(
            htmls[3],
            ParentNode(
                "ul",
                [
                    LeafNode("li", "many"),
                    LeafNode("li", "dashes"),
                    LeafNode("li", "here"),
                ],
            ),
        )

    def test_ordered_to_html(self):
        lists = [
            "1. Single item",
            "1. more\n2. than\n3. one\n4. item",
        ]

        htmls = list(map(ordered_to_html, lists))

        self.assertEqual(htmls[0], ParentNode("ol", [LeafNode("li", "Single item")]))

        self.assertEqual(
            htmls[1],
            ParentNode(
                "ol",
                [
                    LeafNode("li", "more"),
                    LeafNode("li", "than"),
                    LeafNode("li", "one"),
                    LeafNode("li", "item"),
                ],
            ),
        )
