from pathlib import Path
import shutil
import converters as conv

def copy_directory(src_dir, tgt_dir):
    # Make target if not exists, plus parents.
    # I've written enough recursive directory tree walkers inm my life. I'm done with that noise.
    tgt_path = Path(tgt_dir)
    src_path = Path(src_dir)
    if tgt_path.exists():
        shutil.rmtree(tgt_dir)
    tgt_path.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src=src_path, dst=tgt_path, dirs_exist_ok=True)

def generate_page(src_path, tmpl_path, tgt_path):
    print(f'Generating page from {src_path} using {tmpl_path}')
    with open(Path(src_path), 'r') as f:
        markdown = f.read()
    title = conv.extract_title(markdown)
    html_content = conv.markdown_to_html_node(markdown).to_html()
    with open(Path(tmpl_path),'r') as f:
        template = f.read().replace(r'{{ Title }}', title).replace(r'{{ Content }}', html_content)
    with open(Path(tgt_path), 'w') as f:
        f.write(template)


def generate_pages_recursive(src_path, tmpl_path, tgt_path, root=''):
    if root == '':
        root = src_path
    for pth in Path(root).iterdir():
        pthstr = str(pth).replace(src_path,tgt_path)
        # print(str(pth).replace(src_path,tgt_path))
        # print(str(pth).replace(str(src_path), str(tgt_path)))
        if pth.is_dir():
            Path.mkdir(Path(pthstr))
            generate_pages_recursive(src_path, tmpl_path, tgt_path, pth)
            continue
        fpath = pthstr.replace('.md','.html')
        generate_page(pth, tmpl_path, fpath)
        
if __name__=='__main__':
    copy_directory('static','public')
    generate_pages_recursive('content/','template.html','public/')

