from leafnode import LeafNode
from enum import Enum

TextType = Enum("TextType", ["text", "bold", "italic", "code", "link", "image"])


class TextNode:
    def __init__(self, text, text_type: TextType, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textNode) -> bool:
        return (
            self.text == textNode.text
            and self.text_type == textNode.text_type
            and self.url == textNode.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.text:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.bold:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.italic:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.code:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.link:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.image:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
