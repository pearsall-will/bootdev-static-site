from textnode import TextNode

class HTMLNode:

    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ''
        return ''.join([f' {k}="{v}"' for k,v in self.props.items()])

    def __eq__(self, node):
        return (isinstance(node, HTMLNode) 
                and self.tag == node.tag
                and self.value == node.value
                and self.children == node.children
                and self.props == node.props)

    def __repr__(self):
        childs = "\n\t"+"\n\t".join([str(c) for c in self.children]) if self.children else "None"
        return (f'HTMLNode(Tag: {self.tag},Value: {self.value},Children: {childs} , Props: {self.props})')

class LeafNode(HTMLNode):

    def __init__(self, tag: str=None, value: str=None, props: dict=None):
        self = super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value and self.tag != 'img':
            print(self.__dict__)
            raise ValueError("LeafNode requires a Value")
        if self.tag:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return self.value

class ParentNode(HTMLNode):

    def __init__(self, tag: str = None, children: list = [], props: dict = None):
        self = super().__init__(children=children, tag=tag, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag Expected")
        if not self.children:
            raise ValueError("Children Expected")
        return f'<{self.tag}{self.props_to_html()}>{"".join([c.to_html() for c in self.children])}</{self.tag}>'


def text_node_to_html_node(node: TextNode):
    if node.text_type not in ["text","bold","italic","code","link","image"]:
        raise Exception("Bad text_type")

    tags = {"text": None, "bold":'b', "italic":'i', "code":'code', "link":'a', "image":'img',}
    props = {"text": None, "bold": None, "italic": None, "code": None,
             "link": {"href": node.url}, "image": {"src": node.url, "alt":node.text},}
    if node.text_type == "image":
        value = None
    else:
        value = node.text
    return LeafNode(tag=tags[node.text_type], value=value, props=props[node.text_type])
