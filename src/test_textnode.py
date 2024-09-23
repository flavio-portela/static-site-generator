import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_link,
    split_node_delimeter,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_images,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)
        # equal with URL
        node3 = TextNode("This is a text node", TextType.bold, "https://url.com")
        node4 = TextNode("This is a text node", TextType.bold, "https://url.com")
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        # test equality when text is different
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node 2", TextType.bold)
        self.assertNotEqual(node, node2)
        # test equality when text_type is different
        node3 = TextNode("This is a text node", TextType.bold)
        node4 = TextNode("This is a text node", TextType.italic)
        self.assertNotEqual(node3, node4)
        # test equality when URL is different
        node5 = TextNode("This is a text node", TextType.bold, "https://url1.com")
        node6 = TextNode("This is a text node", TextType.bold, "https://url2.com")
        self.assertNotEqual(node5, node6)

    def test_url_default_to_none(self):
        node = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node.url, None)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(text="This is a text node", text_type=TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_immage(self):
        node = TextNode(
            text="This is an image",
            text_type=TextType.image,
            url="https://image-example.com",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://image-example.com", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode(text="This is bold", text_type=TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode(
            "This is text with a `code block` word.", text_type=TextType.text
        )
        new_nodes = split_node_delimeter([node], "`")
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("code block", TextType.code),
                TextNode(" word.", TextType.text),
            ],
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )
        matches = extract_markdown_link("This is a text without matches")
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_link(text)
        self.assertEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )
        matches = extract_markdown_link("This is a text without matches")
        self.assertEqual([], matches)


class TestSplitNodeImages(unittest.TestCase):
    def test_split_node_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        node = TextNode(text, TextType.text)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.text),
                TextNode("to boot dev", TextType.link, "https://www.boot.dev"),
                TextNode(" and ", TextType.text),
                TextNode(
                    "to youtube", TextType.link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_node_images(self):
        text = "This is text with a link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(
            text,
            TextType.text,
        )
        new_nodes = split_nodes_images([node])

        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.text),
                TextNode(
                    "rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.text),
                TextNode("obi wan", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )
        # Test with a single link
        text = "This is text with a link ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        node = TextNode(
            text,
            TextType.text,
        )
        new_nodes = split_nodes_images([node])

        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.text),
                TextNode(
                    "rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif"
                ),
            ],
            new_nodes,
        )
        # Test without link
        text = "This is text with a link"
        node = TextNode(
            text,
            TextType.text,
        )
        new_nodes = split_nodes_images([node])

        self.assertEqual(
            [
                TextNode("This is text with a link", TextType.text),
            ],
            new_nodes,
        )
        # Test with a link at the beginning
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a link"
        node = TextNode(
            text,
            TextType.text,
        )
        new_nodes = split_nodes_images([node])

        self.assertEqual(
            [
                TextNode(
                    "rick roll", TextType.image, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" This is text with a link", TextType.text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
