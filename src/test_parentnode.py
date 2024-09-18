import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        result = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(result, expected)
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(tag="p", children=[
                    LeafNode("b", "Bold text"),
                ]),
            ],
        )
                                                                                     
        result = node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b></p></p>"
        self.assertEqual(result, expected)
