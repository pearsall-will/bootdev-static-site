import unittest
from converters import *
from htmlnode import *
from textnode import *

class test_converters(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title('# title'),'title')

    def test_extract_title_not_top(self):
        self.assertEqual(extract_title('\n\n\n# title'), 'title')

    def test_extract_title_no_title_raises(self):
        with self.assertRaisesRegex(Exception,"No header found"):
            extract_title('no title here bucko.\n## psyche.')

    def test_text_node_to_html_node_text(self):
        node = text_node_to_html_node(TextNode("This is a text node", "text", url="www.google.com"))
        lnode = LeafNode(value="This is a text node")

        self.assertEqual(node, lnode)

    def test_text_node_to_html_node_bold(self):
        node = text_node_to_html_node(TextNode("This is a text node", "bold", url="www.google.com"))        
        lnode = LeafNode(value="This is a text node", tag="b")

        self.assertEqual(node, lnode)

    def test_text_node_to_html_node_italic(self):
        node = text_node_to_html_node(TextNode("This is a text node", "italic", url="www.google.com"))        
        lnode = LeafNode(value="This is a text node", tag="i")

        self.assertEqual(node, lnode)

    def test_text_node_to_html_node_code(self):
        node = text_node_to_html_node(TextNode("This is a text node", "code", url="www.google.com"))        
        lnode = LeafNode(value="This is a text node", tag="code")

        self.assertEqual(node, lnode)

    def test_text_node_to_html_node_link(self):
        node = text_node_to_html_node(TextNode("This is a text node", "link", url="www.google.com"))        
        lnode = LeafNode(value="This is a text node", tag="a",props={"href": "www.google.com"})

        self.assertEqual(node, lnode)

    def test_text_node_to_html_node_image(self):
        node = text_node_to_html_node(TextNode("AltText","image", "www.google.com/image1.png"))
        lnode = LeafNode(tag="img",props={"src":"www.google.com/image1.png","alt":"AltText"})
        self.assertEqual(node, lnode)

    def test_markdown_to_blocks(self):
        blocks = ['# This is a heading','This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                  '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        text ='''# This is a heading



                This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                * This is the first list item in a list block
                * This is a list item
                * This is another list item'''
        self.assertEqual(blocks, markdown_to_blocks(text))

    def test_block_to_blocktype_heading1(self):
        self.assertEqual(block_to_blocktype('# head'), "heading")

    def test_block_to_blocktype_heading2(self):
        self.assertEqual(block_to_blocktype('## head'), "heading")

    def test_block_to_blocktype_heading3(self):
        self.assertEqual(block_to_blocktype('### head'), "heading")

    def test_block_to_blocktype_heading4(self):
        self.assertEqual(block_to_blocktype('#### head'), "heading")

    def test_block_to_blocktype_heading5(self):
        self.assertEqual(block_to_blocktype('##### head'), "heading")

    def test_block_to_blocktype_heading6(self):
        self.assertEqual(block_to_blocktype('###### head'), "heading")
    
    def test_block_to_blocktype_heading_bad(self):
        self.assertEqual(block_to_blocktype('####### head'), "paragraph")

    def test_block_to_blocktype_code1(self):
        block = """```python\n python code block.\n```"""
        self.assertEqual(block_to_blocktype(block), 'code')

    def test_block_to_blocktype_code2(self):
        block = """```javascript\n javascript code block.\n\nr\n\n   r\n```"""
        self.assertEqual(block_to_blocktype(block), 'code')

    def test_block_to_blocktype_code_bad(self):
        block = """```python\n python code block.\n``` """
        self.assertEqual(block_to_blocktype(block), 'paragraph')

    def test_block_to_blocktype_quote1(self):
        block = '''>quote'''
        self.assertEqual(block_to_blocktype(block),'quote')
    def test_block_to_blocktype_quote2(self):
        block = '''>quote\n>quoteline2\r\n>'''
        self.assertEqual(block_to_blocktype(block),'quote')

    def test_block_to_blocktype_quote_bad(self):
        block = '''>quote\nlinetwo\n>'''
        self.assertEqual(block_to_blocktype(block),'paragraph')

    def test_block_to_blocktype_unordered_list1(self):
        block = """* I'm a list"""
        self.assertEqual(block_to_blocktype(block), 'unordered_list')

    def test_block_to_blocktype_unordered_list2(self):
        block = """* I'm a list\n* line 2"""
        self.assertEqual(block_to_blocktype(block), 'unordered_list')

    def test_block_to_blocktype_unordered_list3(self):
        block = """* I'm a list\n- line 2\n* line 3"""
        self.assertEqual(block_to_blocktype(block), 'unordered_list')

    def test_block_to_blocktype_unordered_bad(self):
        block = """* I'm a list\n line 2\n* line 3"""
        self.assertEqual(block_to_blocktype(block), 'paragraph')

    def test_block_to_blocktype_ordered_list1(self):
        block = """1. item1"""
        self.assertEqual(block_to_blocktype(block), 'ordered_list')

    def test_block_to_blocktype_ordered_list2(self):
        block = """1. item1\n2. item2\n3. item3"""
        self.assertEqual(block_to_blocktype(block), 'ordered_list')

    def test_block_to_blocktype_ordered_list_big(self):
        block = ("1. item1\n"
                 "2. item2\n"
                 "3. item3\n"
                 "4. item4\n"
                 "5. item5\n"
                 "6. item6\n"
                 "7. item7\n"
                 "8. item8\n"
                 "9. item9\n"
                 "10. item10\n"
                 "11. item11\n"
                 "12. item12\n"
                 "13. item13\n"
                 "14. item14\n"
                 "15. item15\n"
                 "16. item16\n"
                 "17. item17\n"
                 "18. item18\n"
                 "19. item19\n"
                 "20. item20")
        self.assertEqual(block_to_blocktype(block), 'ordered_list')

    def test_block_to_blocktype_ordered_list_bad_numbering(self):
        block = """1. item1\n3. item3"""
        self.assertEqual(block_to_blocktype(block), 'paragraph')

    def test_block_to_blocktype_ordered_list_bad_line(self):
        block = """1. item1\nbadline\n2. item2"""
        self.assertEqual(block_to_blocktype(block), 'paragraph')

    def test_block_to_blocktype_paragraph(self):
        block = """lol I'm just plain old text bro"""
        self.assertEqual(block_to_blocktype(block), 'paragraph')

class test_markdown_to_html_node(unittest.TestCase):
    def test_simple(self):
        md = '# heading'
        html = markdown_to_html_node(md)
        htmlnode2 = hnode.ParentNode('div',[LeafNode('h1','heading')]
            )
        self.assertEqual(html,htmlnode2)

    # def test_simplish(self):
    #     md = '''# heading

    #             This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    #             * This is the first list item in a list block
    #             * This is a list item
    #             * This is another list item'''
    #     html = markdown_to_html_node(md)
    #     htmlnode2 = hnode.ParentNode('div',[
    #         hnode.LeafNode('h1','heading'),
    #         hnode.ParentNode('p',
    #             [hnode.LeafNode(None,'This is a paragraph of text. It has some '),
    #              hnode.LeafNode('b','bold'),
    #              hnode.LeafNode(None,' and '),
    #              hnode.LeafNode('i','italic'),
    #              hnode.LeafNode(None,' words inside of it.')]),
    #         hnode.ParentNode('ul',[
    #             hnode.LeafNode('li','This is the first list item in a list block'),
    #             hnode.LeafNode('li','This is a list item'),
    #             hnode.LeafNode('li','This is another list item')
    #         ])
    #     ])
    #     self.assertEqual(html,htmlnode2)

    # def test_very_complex(self):
    #     # Complex case that should include all node types, images, and links as well.
    #     md = (
    #         "# Heading Test\n\n"
    #         "The above is a heading. This is a paragraph\n"
    #         "**Bold Text\n**"
    #         "*italics*\n\n"
    #         "## Ordered List Test\n\n"
    #         "1. Item 1\n"
    #         "2. Item 2\n"
    #         "3. Item 3\n\n"
    #         "### Unordered List\n\n"
    #         "* item 1\n"
    #         "* item 2\n"
    #         "- Item 3\n\n"
    #         "#### Code Block\n\n"
    #         "```"
    #         "This is a code block.\n"
    #         "```\n\n"
    #         "###### Links and Images\n\n"
    #         "### Links\n"
    #         "[linkname](www.google.com/link)\n"
    #         "[linkname2](www.google.com/link)\n"
    #         "[linkname3](www.google.com/link)\n\n"
    #         "## Images\n\n"
    #         "![imagealttext](www.google.com/image)\n"
    #         "![imagealttext2](www.google.com/image)\n"
    #         "![imagealttext3](www.google.com/image)")
    #     html = markdown_to_html_node(md)

    #     html2 = ParentNode('div',children=[
    #         LeafNode('h1','Heading Test'),
    #         ParentNode('p',children=[
    #             LeafNode(None,'The above is a heading. This is a paragraph'),
    #             LeafNode('b','Bold Text'),
    #             LeafNode('i','italics')
    #         ]),
    #         LeafNode('h2','Ordered List Test'),
    #         ParentNode('ol',children=[
    #             LeafNode('li','Item 1'),
    #             LeafNode('li','Item 2'),
    #             LeafNode('li','Item 3')
    #         ]),
    #         LeafNode('h3','Unordered List'),
    #         ParentNode('ul',children=[
    #             LeafNode('li','item 1'),
    #             LeafNode('li','item 2'),
    #             LeafNode('li','Item 3')
    #         ]),
    #         LeafNode('h4','Code Block'),
    #         LeafNode('code','This is a code block.'),
    #         LeafNode('h6','Links and Images'),
    #         LeafNode('h3','Links'),
    #         ParentNode('p',children=[
    #             LeafNode('a','linkname',props={'href':'www.google.com/link'}),
    #             LeafNode('a','linkname2',props={'href':'www.google.com/link'}),
    #             LeafNode('a','linkname3',props={'href':'www.google.com/link'}),
    #         ]),
    #         LeafNode('h2','Images'),
    #         ParentNode('p',children=[
    #             LeafNode('img',props={'src':'www.google.com/image','alt':'imagealttext'}),
    #             LeafNode('img',props={'src':'www.google.com/image','alt':'imagealttext2'}),
    #             LeafNode('img',props={'src':'www.google.com/image','alt':'imagealttext3'})
    #         ])
    #     ])