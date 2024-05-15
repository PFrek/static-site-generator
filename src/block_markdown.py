from htmlnode import LeafNode, ParentNode
from textnode import text_to_textnodes, text_node_to_html_node


class BlockType:
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    cur_block = ""
    for line in markdown.split("\n"):
        stripped = line.strip()
        if len(stripped) > 0:
            if len(cur_block) > 0:
                cur_block += "\n"
            cur_block += stripped
        else:
            if len(cur_block) > 0:
                blocks.append(cur_block)
                cur_block = ""

    if len(cur_block) > 0:
        blocks.append(cur_block)

    return blocks


def block_to_block_type(block):
    if check_heading_start(block):
        return BlockType.heading

    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.code

    is_quote = True
    is_unordered = True
    is_ordered = True
    next_num = 1

    lines = block.split("\n")
    for line in lines:
        if not check_line_start(line, ">"):
            is_quote = False

        if not check_line_start(line, "* ") and not check_line_start(line, "- "):
            is_unordered = False

        ordered, next_num = check_ordered_start(line, next_num)
        if not ordered:
            is_ordered = False

    if is_quote:
        return BlockType.quote

    if is_unordered:
        return BlockType.unordered_list

    if is_ordered:
        return BlockType.ordered_list

    return BlockType.paragraph


def check_line_start(line, symbol):
    if len(symbol) > len(line):
        return False

    for i in range(len(symbol)):
        if line[i] != symbol[i]:
            return False

    return True


def check_ordered_start(line, next_num):
    return (check_line_start(line, f"{next_num}. "), next_num + 1)


def check_heading_start(line):
    is_heading = False

    for i in range(1, 7):
        heading_start = "#" * i + " "

        if check_line_start(line, heading_start):
            is_heading = True
            break

    return is_heading


def content_to_nodes(content):
    return list(map(text_node_to_html_node, text_to_textnodes(content)))


def paragraph_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.paragraph:
        raise ValueError(f"Expected a paragraph block, got a '{block_type}'")

    children = content_to_nodes(block)

    return ParentNode("p", children)


def get_quote_contents(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.quote:
        raise ValueError(f"Expected a quote block, got a '{block_type}'")

    return block.strip("> ")


def quote_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.quote:
        raise ValueError(f"Expected a quote block, got a '{block_type}'")

    children = []
    for line in block.split("\n"):
        contents = get_quote_contents(line) + "<br>"
        children.extend(content_to_nodes(contents))

    return ParentNode("blockquote", children)


def get_code_contents(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.code:
        raise ValueError(f"Expected a code block, got a '{block_type}'")

    return block[3:-3].strip()


def code_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.code:
        raise ValueError(f"Expected a code block, got a '{block_type}'")

    contents = get_code_contents(block)

    return ParentNode("pre", [LeafNode("code", contents)])


def get_heading_contents(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.heading:
        raise ValueError(f"Expected a heading block, got a '{block_type}'")

    return block.strip("# ")


def get_heading_level(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.heading:
        raise ValueError(f"Expected a heading block, got a '{block_type}'")

    level = 0

    for i in range(len(block)):
        if block[i] != "#":
            break

        level += 1

    return level


def heading_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.heading:
        raise ValueError(f"Expected a heading block, got a '{block_type}'")

    contents = get_heading_contents(block)
    level = get_heading_level(block)

    children = content_to_nodes(contents)

    return ParentNode(f"h{level}", children)


def get_unordered_items(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.unordered_list:
        raise ValueError(f"Expected a unordered_list block, got a '{block_type}'")

    contents = []
    for line in block.split("\n"):
        if line[0] == "*":
            pattern = "* "
        elif line[0] == "-":
            pattern = "- "
        else:
            pattern = ""

        contents.append(line.strip(pattern))

    return contents


def unordered_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.unordered_list:
        raise ValueError(f"Expected a unordered_list block, got a '{block_type}'")

    html = ParentNode("ul", [])

    items = get_unordered_items(block)
    for item in items:
        children = content_to_nodes(item)
        html.children.append(ParentNode("li", children))

    return html


def get_ordered_items(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.ordered_list:
        raise ValueError(f"Expected a ordered_list block, got a '{block_type}'")

    contents = []
    for line in block.split("\n"):
        contents.append(line.strip("123456789. "))

    return contents


def ordered_to_html(block):
    block_type = block_to_block_type(block)
    if block_type != BlockType.ordered_list:
        raise ValueError(f"Expected a ordered_list block, got a '{block_type}'")

    html = ParentNode("ol", [])

    items = get_ordered_items(block)
    for item in items:
        children = content_to_nodes(item)
        html.children.append(ParentNode("li", children))

    return html


def block_to_html(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.paragraph:
        return paragraph_to_html(block)
    if block_type == BlockType.heading:
        return heading_to_html(block)
    if block_type == BlockType.quote:
        return quote_to_html(block)
    if block_type == BlockType.code:
        return code_to_html(block)
    if block_type == BlockType.unordered_list:
        return unordered_to_html(block)
    if block_type == BlockType.ordered_list:
        return ordered_to_html(block)

    raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        children.append(block_to_html(block))

    return ParentNode("div", children)
