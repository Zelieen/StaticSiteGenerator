import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq_props_to_html(self):
        node = HTMLNode("tag", "text_content", "child", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_eq_NotImplementedError(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_eq(self):
        node = HTMLNode("tag", "text_content", "child", {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("tag", "text_content", "child", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("tag", "text_content", "child", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(repr(node), 'HTMLNode - tag: tag, value: text_content, children: child, props:  href="https://www.google.com" target="_blank"')

    def test_props_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_render(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_render_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node, node2)

    def test_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_tag_none(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

if __name__ == "__main__":
    unittest.main()