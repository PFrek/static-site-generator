import re
from htmlnode import LeafNode


class TextNode:
    type_text = "text"
    type_bold = "bold"
    type_italic = "italic"
    type_code = "code"
    type_link = "link"
    type_image = "image"

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextNode.text_type_text:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextNode.type_bold:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextNode.type_italic:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextNode.type_code:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextNode.type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextNode.type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError(f"Invalid TextNode text_type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextNode.type_text:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: missing closing {delimiter}")

        for i in range(len(parts)):
            if len(parts[i]) == 0:
                continue

            if i % 2 == 1:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                new_nodes.append(TextNode(parts[i], TextNode.type_text))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextNode.type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text
        for image_text, image_url in images:
            parts = original_text.split(f"![{image_text}]({image_url})", 1)

            if len(parts[0]) > 0:
                new_nodes.append(TextNode(parts[0], TextNode.type_text))

            new_nodes.append(TextNode(image_text, TextNode.type_image, image_url))

            original_text = parts[1]

        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, TextNode.type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextNode.type_text:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        original_text = node.text
        for link_text, link_url in links:
            parts = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(parts[0]) > 0:
                new_nodes.append(TextNode(parts[0], TextNode.type_text))

            new_nodes.append(TextNode(link_text, TextNode.type_link, link_url))

            original_text = parts[1]

        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, TextNode.type_text))

    return new_nodes


def extract_markdown_images(text):
    regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches


def extract_markdown_links(text):
    regex = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(regex, text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextNode.type_text)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextNode.type_bold)
    nodes = split_nodes_delimiter(nodes, "*", TextNode.type_italic)
    nodes = split_nodes_delimiter(nodes, "`", TextNode.type_code)

    return nodes
