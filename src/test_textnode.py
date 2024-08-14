import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("This is a text node", "")
        node2 = TextNode("This is a text node", "")
        self.assertEqual(node, node2)
    
    def test_eq3(self):
        node = TextNode("This is a text node", "bold", url="www.google.com")
        node2 = TextNode("This is a text node", "bold", url="www.google.com")
        self.assertEqual(node, node2)
    
    def test_noteq1(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "plain")
        self.assertNotEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", "bold", url="www.google.com")
        node2 = TextNode("This is a text node", "plain")
        self.assertNotEqual(node, node2)

    def test_noteq3(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", url="www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_splitter_code(self):
        node = TextNode("This is text with a `code block` word", 'text')
        new_nodes = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(new_nodes,[
                TextNode("This is text with a ", 'text'),
                TextNode("code block", 'code'),
                TextNode(" word", 'text'),
            ])

    def test_splitter_bold(self):
        node = TextNode("This is text with* a **code block** word", 'text')
        new_nodes = split_nodes_delimiter([node], "**", 'bold')
        self.assertEqual(new_nodes,[
                TextNode("This is text with* a ", 'text'),
                TextNode("code block", 'bold'),
                TextNode(" word", 'text'),
            ])

    def test_splitter_italic(self):
        node = TextNode("This is text with a *code block* word", 'text')
        new_nodes = split_nodes_delimiter([node], "*", 'italic')
        self.assertEqual(new_nodes,[
                TextNode("This is text with a ", 'text'),
                TextNode("code block", 'italic'),
                TextNode(" word", 'text'),
            ])

    def test_split_nodes_with_url_link(self):
    
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            'text')
        new_nodes = split_nodes_with_url([node], url_type='link')
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'link', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'link', "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_split_nodes_with_url_image(self):
    
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            'text')
        new_nodes = split_nodes_with_url([node], url_type='image')
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'image', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'image', "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            'text')
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'link', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'link', "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_split_nodes_image(self):
    
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            'text')
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'image', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'image', "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_split_nodes_with_url_link_list(self):
    
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            'text')
        new_nodes = split_nodes_with_url([node,node], url_type='link')
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'link', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'link', "https://www.youtube.com/@bootdotdev"
                ),
            TextNode("This is text with a link ", 'text'),
            TextNode("to boot dev", 'link', "https://www.boot.dev"),
            TextNode(" and ", 'text'),
            TextNode(
                "to youtube", 'link', "https://www.youtube.com/@bootdotdev"
                ),
            ])

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        data = [
            TextNode("This is ", 'text'),
            TextNode("text", 'bold'),
            TextNode(" with an ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" word and a ", 'text'),
            TextNode("code block", 'code'),
            TextNode(" and an ", 'text'),
            TextNode("obi wan image", 'image', "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),]
        self.assertEqual(text_to_textnodes(text),data)

    def test_text_to_textnodes2(self):
        text = 'This is text with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and [link](https://boot.dev)'
        data = [
            TextNode("This is text with an ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" word and a ", 'text'),
            TextNode('code block', 'code'),
            TextNode(" and an ", 'text'),
            TextNode("obi wan image", 'image', "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),
            TextNode(" and ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),]


if __name__ == "__main__":
    unittest.main()
