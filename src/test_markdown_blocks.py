import unittest

##from textnode import TextNode, TextType, text_node_to_html_node
##from inline_markdown import *
from markdown_blocks import *


class Testinline_markdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type(self):
        md = """## Welcome to the Dungeon"""
        blocks = markdown_to_blocks(md)
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_olist(self):
        md = """
1. This is the **first** item
2. This is the second item with _italic_
3. This is the third item with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the <b>first</b> item</li><li>This is the second item with <i>italic</i></li><li>This is the third item with <code>code</code></li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
