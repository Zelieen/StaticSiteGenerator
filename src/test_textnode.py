import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url_default(self):
        node = TextNode("This is a None test", TextType.LINK, None)
        node2 = TextNode("This is a None test", TextType.LINK)
        self.assertEqual(node, node2)

    def test_eq_type(self):
        node = TextNode("This is a Type test", TextType.IMAGE)
        node2 = TextNode("This is a Type test", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, text, https://www.boot.dev)")

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_eq_text(self):
        node = TextNode("This is a different text", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
