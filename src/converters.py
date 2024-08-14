import htmlnode as hnode
import textnode as tnode
import re

def extract_title(markdown: str) -> str:
    for line in markdown.split('\n'):
        if line[:2]=='# ':
            return line.split(' ')[1]
    raise Exception("No header found")
    
def text_node_to_html_node(node: tnode.TextNode):
    if node.text_type not in ["text","bold","italic","code","link","image"]:
        raise Exception("Bad text_type")

    tags = {"text": None, "bold":'b', "italic":'i', "code":'code', "link":'a', "image":'img',}
    props = {"text": None, "bold": None, "italic": None, "code": None,
             "link": {"href": node.url}, "image": {"src": node.url, "alt":node.text},}
    if node.text_type == "image":
        value = None
    else:
        value = node.text
    return hnode.LeafNode(tag=tags[node.text_type], value=value, props=props[node.text_type])


def markdown_to_blocks(markdown: str):
    return ['\n'.join([line.strip() for line in block.strip().strip('\n\n').split('\n')])
            for block in markdown.split('\n\n') if block != '']

def block_to_blocktype(block: str) -> str:
    # Strip windows nonsense.
    block = block.replace('\r','')
    if re.match(r'^#{1,6} ', block):
        return 'heading'
    if re.match('^```(.*\n)*```$', block):
        return 'code'
    # split checks
    splitblock = block.split('\n')
    try:
        if all([line[0]=='>' for line in splitblock]):
            return 'quote'
        if all([(line[1]==' ' and line[0] in ('*','-')) for line in splitblock]):
            return 'unordered_list'
        if all([(line.split(' ')[0]==f'{i+1}.') for i, line in enumerate(splitblock)]):
            return 'ordered_list'
    except IndexError as e:
        return 'paragraph'
    return 'paragraph'


def get_heading_tuple(head_block: str):
    head, content = head_block.split(' ', 1)
    content = [text_node_to_html_node(node) for node in tnode.text_to_textnodes(content)]
    return f'h{head.count("#")}', content


def markdown_to_html_node(markdown):
    children = []
    for block in markdown_to_blocks(markdown):
        btype = block_to_blocktype(block)
        if btype=='code':
            children.append(hnode.LeafNode('code',block[3:-3]))
        elif btype=='quote':
            children.append(hnode.LeafNode('blockquote',block[1:].replace('\n>','\n').strip()))
        elif btype=='heading':
            htag, hcontent = get_heading_tuple(block)
            children.append(hnode.ParentNode(htag, hcontent))
        elif btype == 'unordered_list':
            blocks = [line.split(' ',1)[1] for line in block.split('\n')]
            children.append(hnode.ParentNode('ul',[hnode.ParentNode('li',[text_node_to_html_node(nd) for nd in tnode.text_to_textnodes(block)]) for block in blocks]))
        elif btype == 'ordered_list':
            blocks = [line.split(' ',1)[1] for line in block.split('\n')]
            children.append(hnode.ParentNode('ol',[hnode.ParentNode('li',[text_node_to_html_node(nd) for nd in tnode.text_to_textnodes(block)]) for block in blocks]))
        else:
            children.append(
                hnode.ParentNode('p',[text_node_to_html_node(nd) for nd in tnode.text_to_textnodes(block)])
            )
    return hnode.ParentNode('div', children)


if __name__ == '__main__':
    with open('content/majesty/index.md', 'r') as f:
        md = f.read()
    html = markdown_to_html_node(md).to_html()
    print(html)
