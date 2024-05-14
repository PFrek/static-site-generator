from textnode import TextNode
from htmlnode import HTMLNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

    html_node = HTMLNode("p", "Hello world", [node], {"style": "font-family: arial"})
    print(html_node)


main()
