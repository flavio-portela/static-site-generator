from leafnode import LeafNode
from enum import Enum
from typing import Dict
import re

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
def split_node_delimeter(old_nodes: list[TextNode], delimiter: str):
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


def split_nodes_images(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.text:
            matches = extract_markdown_images(node.text)
            if len(matches) > 0:
                splitted_node = []
                text_to_search = node.text
                for match in matches:
                    image_alt, image_link = match
                    sections = text_to_search.split(f"![{image_alt}]({image_link})", 1)
                    if sections[0]:
                        splitted_node.append(TextNode(sections[0], TextType.text))
                    splitted_node.append(
                        TextNode(image_alt, TextType.image, image_link)
                    )
                    if len(matches) == 1 and sections[1]:
                        splitted_node.append(TextNode(sections[1], TextType.text))
                    text_to_search = sections[1]
                new_nodes.extend(splitted_node)
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.text:
            matches = extract_markdown_link(node.text)
            if len(matches) > 0:
                splitted_node = []
                text_to_search = node.text
                for match in matches:
                    link_alt, link_url = match
                    sections = text_to_search.split(f"[{link_alt}]({link_url})", 1)
                    if sections[0]:
                        splitted_node.append(TextNode(sections[0], TextType.text))
                    splitted_node.append(TextNode(link_alt, TextType.link, link_url))
                    if len(matches) == 1 and sections[1]:
                        splitted_node.append(TextNode(sections[1], TextType.text))
                    text_to_search = sections[1]
                new_nodes.extend(splitted_node)
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: str):
    """
    Example:
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_link(text: str):
    """
    Example:
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    """
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches
