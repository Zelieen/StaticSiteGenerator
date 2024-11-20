import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_convert_text(self):
        test_text = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(repr(text_node_to_html_node(test_text)), f"LeafNode(None, This is a text node, None)")
    
    def test_convert_bold(self):
        test_text = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(repr(text_node_to_html_node(test_text)), f"LeafNode(b, This is a text node, None)")

    def test_convert_ital(self):
        test_text = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual((text_node_to_html_node(test_text)).to_html(), "<i>This is a text node</i>")

    def test_convert_link(self):
        test_text = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertEqual((text_node_to_html_node(test_text)).to_html(), '<a href="https://www.boot.dev">This is a text node</a>')

    def test_convert_image(self):
        test_text = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        self.assertEqual((text_node_to_html_node(test_text)).to_html(), '<img src="https://www.boot.dev" alt="This is a text node"></img>')

    def test_convert_error(self):
        test_text = TextNode("This is a text node", TextType.ERROR, "https://www.boot.dev")
        with self.assertRaisesRegex(Exception, "Not a valid text type: TextType.ERROR"):
            (text_node_to_html_node(test_text))   

if __name__ == "__main__":
    unittest.main()
