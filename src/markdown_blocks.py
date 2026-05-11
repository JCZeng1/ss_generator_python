from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    s_markdown = markdown.strip()
    blocks = s_markdown.split('\n\n')
    for block in blocks:
        block = block.strip()
    return blocks


def block_to_block_type(block):
    block_type = BlockType.PARAGRAPH
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(s.startswith(">") for s in block.split("\n")):
        return BlockType.QUOTE
    if all(s.startswith("- ") for s in block.split("\n")):
        return BlockType.ULIST
    if all(s.startswith(f"{index}. ") for index, s in enumerate(block.split("\n"), 1)):
        return BlockType.OLIST
    return block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)  # dispatcher helper
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)


def paragraph_to_html_node(block):
    joined_text = " ".join(block.split("\n"))
    children = text_to_children(joined_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    match = re.match(r"#{1,6} ", block)
    if match:
        count = match.end() - 1
    else:
        raise ValueError("a malformed heading!")
    text = block[count+1:]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)


def code_to_html_node(block):
    if block.startswith("```") and block.endswith("```"):
        text = block[4:-3]
    else:
        raise ValueError("Not a code block")
    text_node = TextNode(text, TextType.TEXT)
    leaf_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [leaf_node])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    text = block.split("\n")
    if all(s.startswith(">") for s in text):
        cleaned = [line.lstrip(">").strip() for line in text]
        joined_text = " ".join(cleaned)
        children = text_to_children(joined_text)
        return ParentNode("blockquote", children)
    else:
        raise ValueError("Not a quote")


def ulist_to_html_node(block):
    text = block.split("\n")
    if all(s.startswith("- ") for s in text):
        cleaned = [line[2:] for line in text]
        li_nodes = []
        for item in cleaned:
            children = text_to_children(item)
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ul", li_nodes)
    else:
        raise ValueError("Not a list")


def olist_to_html_node(block):
    text = block.split("\n")
    if all(s.startswith(f"{index}. ") for index, s in enumerate(text, 1)):
        li_nodes = []
        for index, s in enumerate(text, 1):
            children = text_to_children(s[len(str(index))+2:])
            li_nodes.append(ParentNode("li", children))
        return ParentNode("ol", li_nodes)
    else:
        raise ValueError("Not an ordered list")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    list = []
    for node in text_nodes:
        list.append(text_node_to_html_node(node))
    return list
