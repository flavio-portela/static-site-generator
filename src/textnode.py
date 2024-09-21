from leafnode import LeafNode
from enum import Enum
from typing import Dict

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


# map delimiter to TextType
DelimiterType = Enum("DelimiterType", ["`", "*", "**"])

delimiter_to_text_type: Dict[str, TextType] = {
    "`": TextType.code,
    "*": TextType.italic,
    "**": TextType.bold,
}


# Converts a list of nodes with markdown text into htmml nodes
def split_node_delimeter(
    old_nodes: list[TextNode], delimiter: str
):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            # nothing to parse, include node as is
            new_nodes.append(node)
            continue
        if delimiter in node.text:
            start, end = -1, -1
            for index, char in enumerate(node.text):
                if char == delimiter and start == -1:
                    start = index
                    continue
                if char == delimiter and end == -1:
                    end = index
                    break
            if start == -1 or end == -1:
                raise ValueError("Invalid syintax")
            node_to_convert = node.text[start : end + 1].replace(
                delimiter, ""
            )  # remove the delimiter
            splits = [
                TextNode(text=node.text[0:start], text_type=TextType.text),
                TextNode(
                    text=node_to_convert, text_type=delimiter_to_text_type[delimiter]
                ),
                TextNode(text=node.text[end + 1 :], text_type=TextType.text),
            ]
            new_nodes.extend(splits)

    return new_nodes
