import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_no_value(self):
        node = LeafNode("p")
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(value="just text")
        self.assertEqual(node.to_html(), "just text")
