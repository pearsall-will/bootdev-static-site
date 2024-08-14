import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        nod1 = HTMLNode('h1','Header',[1,2,3],props={'class':'head', "id": 'head1'})
        self.assertEqual(nod1.props_to_html(), ' class="head" id="head1"')

    def test_prop2(self):
        nod1 = HTMLNode('h1','Header',[1,2,3],props=None)
        self.assertEqual(nod1.props_to_html(), '')

    def test_prop3(self):
        nod1 = HTMLNode('h1','Header',[1,2,3],props={'class':'head'})
        self.assertEqual(nod1.props_to_html(), ' class="head"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(),'<p>This is a paragraph of text.</p>')
    def test_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')
    def test_to_html_no_tag(self):
        node = LeafNode(value="raw_text")
        self.assertEqual(node.to_html(), 'raw_text')
    def test_to_html_no_tag_with_props(self):
        node = LeafNode(value="raw_text",props={"class": "lolwat?"})
        self.assertEqual(node.to_html(), 'raw_text')
    def test_value_error(self):
        node = LeafNode(tag='p')
        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),])
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_no_children(self):
        node = ParentNode("p")
        with self.assertRaisesRegex(ValueError,"Children Expected"):
            node.to_html()

    def test_no_tag(self):
        node = ParentNode(children=[LeafNode('p','text')])
        with self.assertRaisesRegex(ValueError,'Tag Expected'):
            node.to_html()

    def test_multi_parent(self):
        node = ParentNode("div",[ParentNode("span",[ParentNode("div",[LeafNode("p","Nested")])])])
        self.assertEqual(node.to_html(), '<div><span><div><p>Nested</p></div></span></div>')

    def test_multi_parent_w_props(self):
        node = ParentNode("div",[ParentNode("span",[ParentNode("div",[LeafNode("p","Nested")])],props={'class':'first'})], props={'class': "top"})
        self.assertEqual(node.to_html(), '<div class="top"><span class="first"><div><p>Nested</p></div></span></div>')
