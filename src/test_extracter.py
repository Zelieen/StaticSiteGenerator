import unittest

from extracter import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_extr_images(self):
        text = "test tuple text with images ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(str(extract_markdown_images(text)), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]")

    def test_only_links(self):
        text = "test tuple text with image + link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        self.assertEqual(str(extract_markdown_links(text)), "[('to boot dev', 'https://www.boot.dev')]")

    def test_only_images(self):
        text = "test tuple text with image + link ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to boot dev](https://www.boot.dev)"
        self.assertEqual(str(extract_markdown_images(text)), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]")

    def test_split(self):
        node =  TextNode("This **ita** est", TextType.TEXT)
        self.assertEqual(str(split_nodes_delimiter(node, "**", TextType.BOLD)), '[TextNode(This , text, None), TextNode(ita, bold, None), TextNode( est, text, None)]')

    def test_split_stretch(self):
        node =  TextNode("This **ita so far** est", TextType.TEXT)
        self.assertEqual(str(split_nodes_delimiter(node, "**", TextType.BOLD)), '[TextNode(This , text, None), TextNode(ita so far, bold, None), TextNode( est, text, None)]')


    def test_split_multi(self):
        node =  TextNode("This *ita* est *rome* anic", TextType.TEXT)
        self.assertEqual(str(split_nodes_delimiter(node, "*", TextType.ITALIC)), '[TextNode(This , text, None), TextNode(ita, italic, None), TextNode( est , text, None), TextNode(rome, italic, None), TextNode( anic, text, None)]')

    def test_split_Exc(self):
        node =  TextNode("Not **ita est", TextType.TEXT)
        with self.assertRaisesRegex(Exception, "Invalid Markdown Syntax: No closing delimiter for TextType.BOLD found."):
            (split_nodes_delimiter(node, "**", TextType.BOLD))

    def test_split_end(self):
        node =  TextNode("This *ita* est `code`", TextType.TEXT)
        self.assertEqual(str(split_nodes_delimiter(node, "`", TextType.CODE)), '[TextNode(This *ita* est , text, None), TextNode(code, code, None)]')

    def test_split_begin(self):
        node =  TextNode("**This** is Sparta", TextType.TEXT)
        self.assertEqual(str(split_nodes_delimiter(node, "**", TextType.BOLD)), '[TextNode(This, bold, None), TextNode( is Sparta, text, None)]')

    def test_image_split(self):
        node =  TextNode("This is text with the image ![to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertEqual(str(split_nodes_image(node)), '[TextNode(This is text with the image , text, None), TextNode(to boot dev, image, https://www.boot.dev)]')

    def test_image_split_end(self):
        node =  TextNode("Start image ![to boot dev](https://www.boot.dev) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_image(node)), '[TextNode(Start image , text, None), TextNode(to boot dev, image, https://www.boot.dev), TextNode( end, text, None)]')

    def test_image_split_start(self):
        node =  TextNode("![to boot dev](https://www.boot.dev) end image", TextType.TEXT)
        self.assertEqual(str(split_nodes_image(node)), '[TextNode(to boot dev, image, https://www.boot.dev), TextNode( end image, text, None)]')

    def test_image_split_2(self):
        node =  TextNode("Start ![to boot dev](https://www.boot.dev) middle ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_image(node)), '[TextNode(Start , text, None), TextNode(to boot dev, image, https://www.boot.dev), TextNode( middle , text, None), TextNode(obi wan, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( end, text, None)]')

    def test_link_split(self):
        node =  TextNode("This is text with the link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(This is text with the link , text, None), TextNode(to boot dev, link, https://www.boot.dev)]')

    def test_link_split_end(self):
        node =  TextNode("Start link [to boot dev](https://www.boot.dev) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(Start link , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( end, text, None)]')

    def test_link_split_start(self):
        node =  TextNode("[to boot dev](https://www.boot.dev) end link", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(to boot dev, link, https://www.boot.dev), TextNode( end link, text, None)]')

    def test_link_split_2(self):
        node =  TextNode("Start [to boot dev](https://www.boot.dev) middle [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(Start , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( middle , text, None), TextNode(obi wan, link, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( end, text, None)]')

    def test_link_split_conflict(self):
        node =  TextNode("Start [to boot dev](https://www.boot.dev) middle ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(Start , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( middle ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end, text, None)]')

    def test_link_split_conflict_last(self):
        node =  TextNode("Start ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) middle [to boot dev](https://www.boot.dev) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(Start ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) middle , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( end, text, None)]')

    def test_link_split_confuse(self):
        node =  TextNode("Start ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) middle [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) end", TextType.TEXT)
        self.assertEqual(str(split_nodes_link(node)), '[TextNode(Start ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) middle , text, None), TextNode(obi wan, link, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( end, text, None)]')

    def test_split_to_nodes(self):
        text = "First test"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(First test, text, None)]')

    def test_split_to_nodes_bold(self):
        text = "Text in **bold**"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None)]')

    def test_split_to_nodes_bold_ital(self):
        text = "Text in **bold**, *italic*"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None), TextNode(, , text, None), TextNode(italic, italic, None)]')

    def test_split_to_nodes_bold_ital_code(self):
        text = "Text in **bold**, *italic* and `code` style with an "
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None), TextNode(, , text, None), TextNode(italic, italic, None), TextNode( and , text, None), TextNode(code, code, None), TextNode( style with an , text, None)]')

    def test_split_to_nodes_bold_ital_code_image(self):
        text = "Text in **bold**, *italic* and `code` style with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None), TextNode(, , text, None), TextNode(italic, italic, None), TextNode( and , text, None), TextNode(code, code, None), TextNode( style with an , text, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg)]')

    def test_split_to_nodes_bold_ital_code_image_txt(self):
        text = "Text in **bold**, *italic* and `code` style with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None), TextNode(, , text, None), TextNode(italic, italic, None), TextNode( and , text, None), TextNode(code, code, None), TextNode( style with an , text, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , text, None)]')

    def test_split_to_nodes_link(self):
        text = "Text with a [link](https://boot.dev)"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text with a , text, None), TextNode(link, link, https://boot.dev)]')
                         
    def test_split_to_nodes_all_types(self):
        text = "Text in **bold**, *italic* and `code` style with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(str(text_to_textnodes(text)), '[TextNode(Text in , text, None), TextNode(bold, bold, None), TextNode(, , text, None), TextNode(italic, italic, None), TextNode( and , text, None), TextNode(code, code, None), TextNode( style with an , text, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , text, None), TextNode(link, link, https://boot.dev)]')

    def test_split_to_blocks(self):
        markdown = None
        self.assertEqual(markdown_to_blocks(markdown), ["None"])

    def test_split_to_blocks_simple(self):
        markdown = "Simple"
        self.assertEqual(markdown_to_blocks(markdown), ["Simple"])

    def test_split_to_blocks_trim(self):
        markdown = " This is text  "
        self.assertEqual(markdown_to_blocks(markdown), ["This is text"])

    def test_split_to_blocks_full(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        self.assertEqual(markdown_to_blocks(markdown), ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.", "* This is the first list item in a list block\n* This is a list item\n* This is another list item"])

    def test_blocker_heading(self):
        block = "# Test head"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_blocker_sub_heading(self):
        block = "### Test subhead"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_blocker_not_heading(self):
        block = "####### too many"
        self.assertEqual(block_to_block_type(block), "normal")

    def test_blocker_code(self):
        block = "```code block```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_blocker_quote(self):
        block = ">quotation"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_blocker_quote_2(self):
        block = ">quotation\n>quote2"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_blocker_quote_faulty(self):
        block = ">quotation\nfaultyquote2"
        self.assertEqual(block_to_block_type(block), "normal")

    def test_blocker_unord(self):
        block = "* list"
        self.assertEqual(block_to_block_type(block), "unordered")

    def test_blocker_unord_alt(self):
        block = "- list"
        self.assertEqual(block_to_block_type(block), "unordered")
        
    def test_blocker_unord_2(self):
        block = "* list\n- two"
        self.assertEqual(block_to_block_type(block), "unordered")
        
    def test_blocker_unord_faulty(self):
        block = "* list\nfaulty"
        self.assertEqual(block_to_block_type(block), "normal")

    def test_blocker_ord(self):
        block = "1. count"
        self.assertEqual(block_to_block_type(block), "ordered")

    def test_blocker_ord_2(self):
        block = "1. count\n2. on"
        self.assertEqual(block_to_block_type(block), "ordered")

    def test_blocker_ord_faulty(self):
        block = "1. count\n0. faulty"
        self.assertEqual(block_to_block_type(block), "normal")

if __name__ == "__main__":
    unittest.main()