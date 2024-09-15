import unittest


from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
        # equal with url
        node3 = TextNode("This is a text node", "bold", "https://url.com")
        node4 = TextNode("This is a text node", "bold", "https://url.com")
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        # test equality when text is different
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node 2", "bold")
        self.assertNotEqual(node, node2)
        # test equality when text_type is different
        node3 = TextNode("This is a text node", "bold")
        node4 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node3, node4)
        # test equality when url is different
        node5 = TextNode("This is a text node", "bold", "https://url1.com")
        node6 = TextNode("This is a text node", "bold", "https://url2.com")
        self.assertNotEqual(node5, node6)

    def test_url_default_to_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)


if __name__ == "__main__":
    unittest.main()
