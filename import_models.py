#!/usr/bin/python3
"""Import 3D models for website page generation."""

import argparse
import os
import os.path
import shutil

GLB_EXT = ".glb"
PNG_EXT = ".png"

from make_pages import find_models


def copy_file(source_dir: str, target_dir: str, filename: str):

    shutil.copy(os.path.join(source_dir, filename), os.path.join(target_dir, filename))


def copy_models(base_dir: str, model_paths: str):

    for model in model_paths:
        target_dir, name = os.path.split(model)
        os.makedirs(target_dir, exist_ok=True)
        source_dir = os.path.join(base_dir, target_dir)
        copy_file(source_dir, target_dir, f"{name}{GLB_EXT}")
        copy_file(source_dir, target_dir, f"{name}{PNG_EXT}")


def import_tree(base_dir: str) -> None:

    current_directory = os.getcwd()
    os.chdir(base_dir)
    model_paths = find_models(".")
    os.chdir(current_directory)

    copy_models(base_dir, model_paths)

    pass


def main():
    parser = argparse.ArgumentParser(
        prog="import_models.py",
        description=f"Imports directory tree containing {GLB_EXT} "
        "and {PNG_EXT} files.",
        epilog="The imported files are copied into a "
        "directory tree based at the current directory.",
    )
    parser.add_argument(
        "--model-root",
        required=True,
        help=f"root of the {GLB_EXT} and {PNG_EXT} directory tree.",
    )
    args = parser.parse_args()

    import_tree(args.model_root)


if __name__ == "__main__":
    main()
