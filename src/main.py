from textnode import *
from gencontent import generate_page, generate_pages_recursive
import os
import shutil
import sys

def prepare_and_copy():
    print(os.getcwd())
    static = './static'
    public = './docs'
    if not os.path.exists(public):
        os.mkdir(public)
    else:
        shutil.rmtree(public)
        os.mkdir(public)
        print(f"Re-generated {public}")
    recursive_copy(static, public)


def recursive_copy(src, dst):
    if not os.path.exists(src):
        raise ValueError("static directory doesn't exist!")

    static_list = os.listdir(src)
    for item in static_list:
        static_item = os.path.join(src, item)
        public_item = os.path.join(dst, item)
        if os.path.isfile(static_item):
            shutil.copy(static_item, public_item)
            print(f"Copied {static_item}")
        elif os.path.isdir(static_item):
            os.mkdir(public_item)
            recursive_copy(static_item, public_item)
        else:
            print("Something strange exists!")


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"Basepath: {basepath}")
    prepare_and_copy()
#    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
