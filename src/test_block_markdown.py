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
    markdown_to_html_node,
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
            self.assertEqual(html, ParentNode("p", [LeafNode(None, block)]))

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

        # block = quotes[0]
        # html = quote_to_html(block)
        # print(html)
        # self.assertEqual(
        #     html, ParentNode("blockquote", [LeafNode(None, "Single line quote")])
        # )

        block = quotes[1]
        html = quote_to_html(block)
        self.assertEqual(
            html,
            ParentNode(
                "blockquote",
                [
                    LeafNode(None, "Multiline"),
                    LeafNode(None, "quotes"),
                    LeafNode(None, "also"),
                    LeafNode(None, "work"),
                ],
            ),
        )

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

            self.assertEqual(html, ParentNode("pre", [LeafNode("code", contents)]))

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

            self.assertEqual(html, ParentNode(f"h{i+1}", [LeafNode(None, contents)]))

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

        self.assertEqual(
            htmls[0],
            ParentNode("ul", [ParentNode("li", [LeafNode(None, "Single item")])]),
        )

        self.assertEqual(
            htmls[1],
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "more")]),
                    ParentNode("li", [LeafNode(None, "than")]),
                    ParentNode("li", [LeafNode(None, "one")]),
                    ParentNode("li", [LeafNode(None, "item")]),
                ],
            ),
        )

        self.assertEqual(
            htmls[2],
            ParentNode("ul", [ParentNode("li", [LeafNode(None, "single dash")])]),
        )

        self.assertEqual(
            htmls[3],
            ParentNode(
                "ul",
                [
                    ParentNode("li", [LeafNode(None, "many")]),
                    ParentNode("li", [LeafNode(None, "dashes")]),
                    ParentNode("li", [LeafNode(None, "here")]),
                ],
            ),
        )

    def test_ordered_to_html(self):
        lists = [
            "1. Single item",
            "1. more\n2. than\n3. one\n4. item",
        ]

        htmls = list(map(ordered_to_html, lists))

        self.assertEqual(
            htmls[0],
            ParentNode("ol", [ParentNode("li", [LeafNode(None, "Single item")])]),
        )

        self.assertEqual(
            htmls[1],
            ParentNode(
                "ol",
                [
                    ParentNode("li", [LeafNode(None, "more")]),
                    ParentNode("li", [LeafNode(None, "than")]),
                    ParentNode("li", [LeafNode(None, "one")]),
                    ParentNode("li", [LeafNode(None, "item")]),
                ],
            ),
        )

    def test_markdown_to_html_node(self):
        markdown = """# This is the title

This is a regular paragraph.
It spans two lines.

* Now an unordered list
* With more than one item
* for good measure

```
// Very good code
int i = 0
i += 1
return i
```

1. Read this markdown
2. Good"""

        html = markdown_to_html_node(markdown)

        self.assertEqual(
            html,
            ParentNode(
                "div",
                [
                    ParentNode("h1", [LeafNode(None, "This is the title")]),
                    ParentNode(
                        "p",
                        [
                            LeafNode(
                                None,
                                "This is a regular paragraph.\nIt spans two lines.",
                            )
                        ],
                    ),
                    ParentNode(
                        "ul",
                        [
                            ParentNode("li", [LeafNode(None, "Now an unordered list")]),
                            ParentNode(
                                "li", [LeafNode(None, "With more than one item")]
                            ),
                            ParentNode("li", [LeafNode(None, "for good measure")]),
                        ],
                    ),
                    ParentNode(
                        "pre",
                        [
                            LeafNode(
                                "code",
                                "// Very good code\nint i = 0\ni += 1\nreturn i",
                            ),
                        ],
                    ),
                    ParentNode(
                        "ol",
                        [
                            ParentNode("li", [LeafNode(None, "Read this markdown")]),
                            ParentNode("li", [LeafNode(None, "Good")]),
                        ],
                    ),
                ],
            ),
        )
