from htmlnode import HTMLNode
from textnode import TextNode, split_nodes_delimiter, extract_markdown_links


def main():
    # node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    # print(node)
    #
    # html_node = HTMLNode("p", "Hello world", [node], {"style": "font-family: arial"})
    # print(html_node)

    text_node = TextNode("This is text with a `code block` word", "text")
    new_nodes = split_nodes_delimiter([text_node], "`", "code")

    print(new_nodes)

    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    print(extract_markdown_links(text))


main()
