import unittest

from converter import markdown_to_html_node, strip_by_md_tags
from htmlnode import HTMLNode, ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_markdown_conversion(self):
        markdown = "simple paragraph"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [ParentNode(tag="p", children=[LeafNode(None, "simple paragraph", None)])])))
    
    def test_text_strip_code(self):
        text = "```code example```"
        self.assertEqual(strip_by_md_tags(text), (["code example"], "pre"))

    def test_text_strip_head1(self):
        text = "# head 1"
        self.assertEqual(strip_by_md_tags(text), (["head 1"], "h1"))

    def test_text_strip_head4(self):
        text = "#### headsub"
        self.assertEqual(strip_by_md_tags(text), (["headsub"], "h4"))

    def test_text_strip_quote(self):
        text = ">quoting here"
        self.assertEqual(strip_by_md_tags(text), (["quoting here"], "blockquote"))

    def test_text_strip_quote2(self):
        text = ">quoting here\n>again"
        self.assertEqual(strip_by_md_tags(text), (["quoting here again"], "blockquote"))

    def test_text_strip_unord(self):
        text = "* list\n- unordered"
        self.assertEqual(strip_by_md_tags(text), (["list", "unordered"], "ul"))

    def test_text_strip_ord(self):
        text = "1. list\n2. ordered"
        self.assertEqual(strip_by_md_tags(text), (["list", "ordered"], "ol"))

    def test_text_strip_text(self):
        text = "plain text"
        self.assertEqual(strip_by_md_tags(text), (["plain text"], "p"))

    def test_markdown_conversion_2_blocks(self):
        markdown = "paragraph1\n\nparagraph2"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [ParentNode(tag="p", children=[LeafNode(None, "paragraph1", None)]),ParentNode(tag="p", children=[LeafNode(None, "paragraph2", None)])])))

    def test_markdown_conversion_2_blocks_header(self):
        markdown = "paragraph1\n\n# paragraph2"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [ParentNode(tag="p", children=[LeafNode(None, "paragraph1", None)]),ParentNode(tag="h1", children=[LeafNode(None, "paragraph2", None)])])))

    def test_markdown_conversion_2_blocks_header_bold(self):
        markdown = "paragraph1\n\n# paragraph **boldi**"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [ParentNode(tag="p", children=[LeafNode(None, "paragraph1", None)]),ParentNode(tag="h1", children=[LeafNode(None, "paragraph ", None),LeafNode("b", "boldi", None)])])))

    def test_markdown_conversion_unordlist_simple(self):
        markdown = "* list unord"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [
            ParentNode(tag="ul", children=[
                ParentNode("li", [LeafNode(None, "list unord", None)])
                ]
                )
                ]
                )))

    def test_markdown_conversion_unordlist(self):
        markdown = "* list\n- unord"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [
            ParentNode(tag="ul", children=[
                ParentNode("li", [LeafNode(None, "list", None)]), 
                ParentNode("li", [LeafNode(None, "unord", None)])]
                )
                ]
                )))
    
    def test_markdown_conversion_code(self):
        markdown = "```code example```"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [
            ParentNode(tag="pre", children=[
                ParentNode("code", [LeafNode(None, "code example", None)]), 
                ]
                )
                ]
                )))

    def test_markdown_conversion_link(self):
        markdown = "**Bold text**[Click me!](https://www.google.com)"
        self.assertEqual(str(markdown_to_html_node(markdown)), str(ParentNode("div", [
            ParentNode(tag="p", children=[
                LeafNode("b", "Bold text", None),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"})]
                ) 
                ]
                ))
                )
        
    def test_md_to_html(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

if __name__ == "__main__":
    unittest.main()