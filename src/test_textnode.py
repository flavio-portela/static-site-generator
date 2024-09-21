import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_node_delimeter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)
        # equal with url
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
        # test equality when url is different
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
        new_nodes = split_node_delimeter([node], "`", TextType.text)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("code block", TextType.code),
                TextNode(" word.", TextType.text),
            ],
        )


if __name__ == "__main__":
    unittest.main()
