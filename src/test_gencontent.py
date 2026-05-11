import unittest

##from textnode import TextNode, TextType, text_node_to_html_node
from markdown_blocks import *
from gencontent import *

class Test_gencontent(unittest.TestCase):
    def test_extract_title(self):
        md = """# Hello"""
        line = extract_title(md)
        self.assertEqual(line, "Hello")


if __name__ == "__main__":
    unittest.main()
