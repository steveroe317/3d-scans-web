#!/usr/bin/python3
"""Generate html for 3D models."""

import os
import os.path

from collections import defaultdict
from string import Template


INDEX_HTML = "index.html"
TEMPLATE_DIR = "templates"
INDEX_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "index.template")
SCAN_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "scan.template")
SCAN_LIST_ITEM_PATH = os.path.join(TEMPLATE_DIR, "scan_list_item.template")

GLB_EXT = ".glb"
PNG_EXT = ".png"
HTML_EXT = ".html"


class MakePagesException(Exception):
    pass


def find_models(base_dir: str) -> list[str]:

    model_path_counts: defaultdict[str, int] = defaultdict(int)

    for dirpath, dirnames, filenames in os.walk(base_dir):

        # Don't walk though hidden directories (specifically .git).
        for dirname in dirnames:
            if dirname.startswith("."):
                dirnames.remove(dirname)

        for filename in filenames:
            if not filename.startswith("."):
                if filename.endswith(GLB_EXT) or filename.endswith(PNG_EXT):
                    model_path = os.path.join(dirpath, filename[: -len(GLB_EXT)])
                    model_path_counts[model_path] += 1

    for model_path in model_path_counts:
        if model_path_counts[model_path] != 2:
            raise MakePagesException(
                f"model {model_path} is missing either a "
                f"{GLB_EXT} or {PNG_EXT} file."
            )

    return list(model_path_counts.keys())


def generate_model_html_files(model_paths: list[str]) -> None:
    """Generate HTML files for model scans."""

    scan_template_file = open(SCAN_TEMPLATE_PATH)
    scan_template = Template(scan_template_file.read())

    for model_path in model_paths:
        model_name = os.path.split(model_path)[-1]

        # Get the model title and .glb filename from the model name.
        model_title = " ".join(model_name.split("-")).title()
        model_glb = model_name + GLB_EXT
        model_depth = len(os.path.split(model_path)) - 1
        if model_depth > 0:
            index_html_path = ".."
            for _ in range(model_depth):
                os.path.join(index_html_path, "..")
            index_html_path = os.path.join(index_html_path, INDEX_HTML)
        else:
            index_html_path = INDEX_HTML

        # Apply subsitutions to the template to get the model html file.
        model_html_path = model_path + HTML_EXT
        model_html_file = open(model_html_path, "w")
        model_html_contents = scan_template.substitute(
            SCAN_TITLE=model_title, SCAN_GLB=model_glb, INDEX_HTML_PATH=index_html_path
        )
        model_html_file.write(model_html_contents)
        model_html_file.close()


def generate_index_html_files(model_paths: list[str]) -> None:
    """Add list of models to index.html file."""

    # Build the lsit of models for the index html file.
    scan_list_item_template_file = open(SCAN_LIST_ITEM_PATH)
    scan_list_item_template = Template(scan_list_item_template_file.read())
    scan_list: str = ""
    model_paths.sort()
    for model_path in model_paths:
        model_name = os.path.split(model_path)[-1]

        # Get the model title and .glb filename from the model name.
        model_title = " ".join(model_name.split("-")).title()
        model_html = model_path + HTML_EXT
        model_png = model_path + PNG_EXT

        scan_list += scan_list_item_template.substitute(
            SCAN_HTML=model_html, SCAN_PNG=model_png, SCAN_TITLE=model_title
        )
        scan_list += "\n"

    # Apply substitutions to the template to get the index html file.
    index_template_file = open(INDEX_TEMPLATE_PATH)
    index_template = Template(index_template_file.read())
    index_html_contents = index_template.substitute(SCAN_LIST=scan_list)
    index_html_file = open(INDEX_HTML, "w")
    index_html_file.write(index_html_contents)
    index_html_file.close()


def main():
    """Validate location and generate web pages."""

    # Require that the templates directory has the expected contents.
    if not os.path.isfile(INDEX_TEMPLATE_PATH):
        raise MakePagesException(f"missing file {INDEX_TEMPLATE_PATH}")
    if not os.path.isfile(SCAN_TEMPLATE_PATH):
        raise MakePagesException(f"missing file {SCAN_TEMPLATE_PATH}")
    if not os.path.isfile(SCAN_LIST_ITEM_PATH):
        raise MakePagesException(f"missing file {SCAN_LIST_ITEM_PATH}")

    # Find all 3D models (GLB files with corresponding PNG files). Unpaired
    # GLB or PNGs are errors.
    model_paths = find_models(os.curdir)

    generate_model_html_files(model_paths)
    generate_index_html_files(model_paths)


if __name__ == "__main__":
    main()
