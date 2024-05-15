import os
import shutil
from block_markdown import markdown_to_html_node


def copy_dir_contents(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        raise ValueError(f"Could not find source dir: {src_dir}")

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    src_contents = os.listdir(src_dir)

    for content in src_contents:
        src_path = os.path.join(src_dir, content)
        dest_path = os.path.join(dest_dir, content)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Making new dir {dest_path}")
            os.mkdir(dest_path)
            copy_dir_contents(src_path, dest_path)


def extract_title(markdown):
    title = ""

    for line in markdown.split("\n"):
        if line.startswith("# "):
            title = line[2:]

    if len(title) == 0:
        raise ValueError("No level 1 heading found in markdown")

    return title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{
          dest_path}' using '{template_path}'")

    markdown = ""
    with open(from_path, "r") as f:
        markdown = f.read()

    template = ""
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, "x") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path_content)

    for entry in dir_contents:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(entry_path):
            if entry[-3:] == ".md":
                generate_page(entry_path, template_path, dest_path[:-3] + ".html")

        else:
            generate_pages_recursive(entry_path, template_path, dest_path)


def main():
    copy_dir_contents("static/", "public/")

    generate_pages_recursive("content/", "template.html", "public/")


main()
