import re
from itertools import zip_longest

image_re = re.compile(r'!\[(.*?)\]\((.*?)\)')
link_re = re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)')
image_re_split = re.compile(r'!\[.*?\]\(.*?\)')
link_re_split = re.compile(r'(?<!!)\[.*?\]\(.*?\)')

URL_REGEX = {
    'link': {
        're': re.compile(r'(?<!!)\[(.*?)\]\((.*?)\)'),
        'split': re.compile(r'(?<!!)\[.*?\]\(.*?\)') },
    'image': {
        're': re.compile(r'!\[(.*?)\]\((.*?)\)'),
        'split': re.compile(r'!\[.*?\]\(.*?\)'),}}

NODE_TYPES ={
    "link": lambda nodes: split_nodes_with_url(nodes, "link"),
    "code": lambda nodes: split_nodes_delimiter(nodes,"`", 'code'),
    "bold": lambda nodes: split_nodes_delimiter(nodes,"**", 'bold'),
    "italic": lambda nodes: split_nodes_delimiter(nodes,"*", 'italic'),
    "image": lambda nodes: split_nodes_with_url(nodes, "image"),
}


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #todo: add logic to catch edge case when we want to split on * so ** won't get caught.
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != 'text':
            new_nodes.append(node)
            continue
        for i,tval in enumerate(node.text.split(delimiter)):
            if i%2==0:
                new_nodes.append(TextNode(tval, 'text'))
            else:
                new_nodes.append(TextNode(tval, text_type))
        if i%2==1:
            raise Exception(f"Missing closing {delimiter}")

    return new_nodes

def split_nodes_with_url(old_nodes: list, url_type: str="link"):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != 'text':
            new_nodes.append(node)
            continue
        l_nodes = [TextNode(url[0],url_type, url[1]) for url in re.findall(URL_REGEX[url_type]['re'],node.text)]
        raw_split=re.split(URL_REGEX[url_type]['split'], node.text)
        while raw_split:
            text = raw_split.pop(0)
            if text != '':
                new_nodes.append(TextNode(text,'text'))
            if l_nodes:
                new_nodes.append(l_nodes.pop(0))
    return new_nodes

def split_nodes_image(old_nodes: list):
    return split_nodes_with_url(old_nodes, 'image')

def split_nodes_link(old_nodes: list):
    return split_nodes_with_url(old_nodes)

def text_to_textnodes(text):
    nodes=[TextNode(text, 'text')]
    for split_funcs in NODE_TYPES.values():
        nodes = split_funcs(nodes)
    return nodes


def main():
    nodes = text_to_textnodes('This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)')
    for node in nodes:
        print(node)
    print("Test 2")
    node = TextNode("This is text with a *code block* word", 'text')
    new_nodes = split_nodes_delimiter([node], "*", 'italic')
    print(new_nodes)

if __name__=='__main__':
    main()