# src/gencontent.py
import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path


def extract_title(md):
    text = md.split("\n")
    for line in text:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header!")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f_md = open(from_path)
    f_tp = open(template_path)
    md = f_md.read()
    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    full_page = f_tp.read().replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    f_md.close()
    f_tp.close()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f_dest = open(dest_path, 'w')
    f_dest.write(full_page)
    f_dest.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    list_content = os.listdir(dir_path_content)
    with open(template_path) as f:
        tp = f.read()
    for item in list_content:
        from_path = os.path.join(dir_path_content, item)
        dest_path = Path(os.path.join(dest_dir_path, item))
        if os.path.isfile(from_path):
            with open(from_path) as f:
                md = f.read()
            html_string = markdown_to_html_node(md).to_html()
            title = extract_title(md)
            full_page = tp.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path.with_suffix(".html"), 'w') as f:
                f.write(full_page)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
