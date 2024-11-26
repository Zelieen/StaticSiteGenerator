import re
from textnode import TextType, TextNode

def extract_markdown_images(text):
    imgs = re.findall(r"!\[(.*?)\]\((.*?)\)", text) # ![alt_text](url)
    return imgs # list of tuples, each tuple contains (alt_text, url)

def extract_markdown_links(text):
    lnks = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text) # (not'!')[anchor_text](url)
    return lnks # list of tuples, each tuple contains (anchor_text, url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if isinstance(old_nodes, TextNode):
        nodes = [old_nodes]
    else:
        nodes = old_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type == TextType.TEXT: #check for delimiter, change here to support other text types (bold, italic), too
            blocks = node.text.split(delimiter)
            if len(blocks) == 1: #the delimiter was not found in node
                new_nodes.append(node)
            elif not len(blocks) % 2: #no matching delimiter pair
                raise Exception(f"Invalid Markdown Syntax: No closing delimiter for {text_type} found.")
            else: #valid delimiters
                start_block = blocks[0]
                end_blocks = delimiter.join(blocks[2:])
                if start_block != "":
                    new_nodes.append(TextNode(start_block, node.text_type))
                new_nodes.append(TextNode(blocks[1], text_type)) # add delimited block to new_nodes
                if end_blocks != "":
                    new_nodes.extend(split_nodes_delimiter(TextNode(end_blocks, node.text_type), delimiter, text_type))
        else: # none Text type nodes are returned as is
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    if isinstance(old_nodes, TextNode):
        nodes = [old_nodes]
    else:
        nodes = old_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT: #change here to support other text types (bold, italic), too
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if images == []: #no images, just return as is
            new_nodes.append(node)
        else: #found images
            image_node = node.text
            for pair in images:
                blocks = image_node.split(f"![{pair[0]}]({pair[1]})", maxsplit = 1)
                start_block = blocks[0]
                if start_block != "":
                    new_nodes.append(TextNode(start_block, node.text_type))
                new_nodes.append(TextNode(pair[0], TextType.IMAGE, pair[1]))
                image_node = blocks[1] #shorten node text
            if blocks[1] != "": #add last block after all images
                new_nodes.append(TextNode(blocks[1], node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    if isinstance(old_nodes, TextNode):
        nodes = [old_nodes]
    else:
        nodes = old_nodes
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT: #change here to support other text types (bold, italic), too
            new_nodes.append(node)
            continue
        images = extract_markdown_links(node.text)
        if images == []: #no links, just return as is
            new_nodes.append(node)
        else: #found links
            image_node = node.text
            for pair in images:
                blocks = re.split(r"(?<!!)\[" + pair[0] + r"\]\(" + pair[1] + r"\)", image_node, maxsplit = 1) #make sure there is no "!" before the link
                start_block = blocks[0]
                if start_block != "":
                    new_nodes.append(TextNode(start_block, node.text_type))
                new_nodes.append(TextNode(pair[0], TextType.LINK, pair[1]))
                image_node = blocks[1] #shorten node text
            if blocks[1] != "": #add last block after all links
                new_nodes.append(TextNode(blocks[1], node.text_type))
    return new_nodes

def text_to_textnodes(text):
    nodes = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes