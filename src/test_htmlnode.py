import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        # returns None if there are no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), None)
