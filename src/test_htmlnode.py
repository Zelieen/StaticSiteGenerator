import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        self.assertEqual(repr(node), "HTMLNode(tag, text_content, children: child, {'href': 'https://www.google.com', 'target': '_blank'})")

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

    def test_parent_html(self):
        node =ParentNode("p", [LeafNode("b", "Bold text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b></p>")

    def test_parent_html_2_children(self):
        node =ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("i", "italic text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><i>italic text</i></p>")

    def test_parent_html_2_nest(self):
        node =ParentNode("p", [LeafNode("b", "Bold text"), ParentNode("p", [LeafNode("i", "italic text"), LeafNode("b", "Bold text")])])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><p><i>italic text</i><b>Bold text</b></p></p>")

    def test_parent_html_props(self):
        node =ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("a", "Click me!", {"href": "https://www.google.com"})], {"parent": "top"})
        self.assertEqual(node.to_html(), '<p parent="top"><b>Bold text</b><a href="https://www.google.com">Click me!</a></p>')

    def test_parent_err(self):
        node = ParentNode(None, ["not tested"])
        with self.assertRaisesRegex(ValueError, "ParentNode must have a tag"):
            node.to_html()       

    def test_parent_no_child(self):
        node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "ParentNode is missing children nodes"):
            node.to_html()

    def test_parent_no_child_2(self):
        node = ParentNode("p", [])
        with self.assertRaisesRegex(ValueError, "ParentNode is missing children nodes"):
            node.to_html() 

    def test_parent_str_child(self):
        node = ParentNode("p", ["catch me"])
        with self.assertRaisesRegex(ValueError, "'catch me' is not a proper child node"):
            node.to_html() 

if __name__ == "__main__":
    unittest.main()