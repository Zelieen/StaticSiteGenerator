from extracter import markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from extracter import text_to_textnodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        #convert by block type, create HTMLnodes
        block_node = create_node_by_type(block)
        #print(block_node)
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes) #wrap all created nodes in ParentNode

def create_node_by_type(block): #creates the ParentNodes with proper tags and adds children nodes
    textlist, tag = strip_by_md_tags(block)
    if tag not in ["pre", "ul", "ol"]:
        parentnodelist = text_to_children(textlist[0])
    else: #add a prefix tag before nested tag
        parentnodelist = []
        nested_tag = "li"
        if tag == "pre":
            nested_tag = "code"
        for text in textlist:
            parentnodelist.append(ParentNode(tag=nested_tag, children=text_to_children(text)))
    #print(f"\nthis is the  parentnodelist: {parentnodelist}\n")
    return ParentNode(tag=tag, children=parentnodelist)

def text_to_children(blocktext): #converts raw markdown text to prcessed TextNodes and then to Leafnodes
    nodelist = []
    for node in text_to_textnodes(blocktext):
        nodelist.append(text_node_to_html_node(node))
    return nodelist #HTMLNodes, mostly LeafNodes

def strip_by_md_tags(block): #separates markdown syntax from text, returns bona fide text and translates syntax to a tag
    match block_to_block_type(block):
        case "heading":
            parts = block.split("# ")
            blocktext = [parts[1]]
            tag = "h" + str(len(parts[0]) + 1) # the number of '#'s
        case "code":
            blocktext = [block[3:-3]]
            tag = "pre"
        case "quote":
            paragraph = []
            lines = block.split("\n")
            for line in lines:
                print(line[1:].strip())
                paragraph.append(line[1:].strip()) #remove leading "<"
            blocktext = [" ".join(paragraph)]
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
            blocktext = [" ".join(block.split("\n"))] #replaces "\n" with " "
            tag = "p"
        case _:
            raise Exception("unknown block type")
    return blocktext, tag