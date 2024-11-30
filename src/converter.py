from extracter import markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from extracter import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        #convert by block type, create node
        block_node = create_node_by_type(block)
        #print(block_node)
        block_nodes.append(block_node)

    #next step: 
    return ParentNode("body", block_nodes)

def create_node_by_type(block):
    textlist, tag = strip_by_md_tags(block)
    if len(textlist) == 1 and tag != "pre":
        parentnodelist = text_to_children(textlist[0])
    else:
        #textnodelist = []
        parentnodelist = []
        nested_tag = "li"
        if tag == "pre":
            nested_tag = "code"
        for text in textlist:
            #textnodelist.append(text_to_children(text))
            parentnodelist.append(ParentNode(tag=nested_tag, children=text_to_children(text)))
        #?? for node in textnodelist:
        #   parentnodelist.append(ParentNode(tag=nested_tag, children=text_to_children(text)))
        #parentnodelist = ParentNode(tag=nested_tag, children=textnodelist)
    print(f"\nthis is the  parentnodelist: {parentnodelist}\n")
    return ParentNode(tag=tag, children=parentnodelist)

def text_to_children(blocktext):
    nodelist = []
    for node in text_to_textnodes(blocktext):
        nodelist.append(text_node_to_html_node(node))
    return nodelist #HTMLnodelist

def strip_by_md_tags(block):
    match block_to_block_type(block):
        case "heading":
            parts = block.split("# ")
            blocktext = [parts[1]]
            tag = "h" + str(len(parts[0]) + 1) # the number of '#'s
        case "code":
            blocktext = [block[3:-3]]
            tag = "pre"
        case "quote":
            blocktext = []
            lines = block.split("\n")
            for line in lines:
                blocktext.append(line[1:])
            tag = "blockquote"
        case "unordered":
            blocktext = []
            lines = block.split("\n")
            for line in lines:
                blocktext.append(line[2:])
            tag = "ul"
        case "ordered":
            blocktext = []
            lines = block.split("\n")
            for line in lines:
                blocktext.append(line[3:])
            tag = "ol"
        case "normal":
            blocktext = [block]
            tag = "p"
        case _:
            raise Exception("unknown block type")
    return blocktext, tag