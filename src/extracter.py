import re

def extract_markdown_images(text):
    imgs = re.findall(r"!\[(.*?)\]\((.*?)\)", text) # ![alt_text](url)
    return imgs # list of tuples, each tuple contains (alt_text, url)

def extract_markdown_links(text):
    lnks = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text) # (not'!')[anchor_text](url)
    return lnks # list of tuples, each tuple contains (anchor_text, url)