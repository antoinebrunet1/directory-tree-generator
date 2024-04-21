import constants
from utils import color_printer
import os


def print_tree(root_directory):
    tree = make_tree(root_directory)

    for line in tree:
        print(line)


def make_tree(root_directory):
    color_printer.init_with_auto_reset()

    tree = []

    add_root(tree, root_directory)
    add_body(tree, root_directory)

    return tree


def add_root(tree, root_directory):
    colored_root_directory = color_printer.get_colored_directory_name(root_directory.name)

    tree.append(f"{colored_root_directory}{os.sep}")
    tree.append(constants.PIPE)


def add_body(tree, root_directory, prefix=""):
    iterator = root_directory.iterdir()
    items = sorted(iterator, key=lambda x: x.is_file())

    for index, item in enumerate(items):
        handle_item(index, item, len(items), tree, prefix)


def handle_item(index, item, items_length, tree, prefix):
    connector = get_connector(index, items_length)

    if item.is_dir():
        generate_directory(tree, item, index, items_length, prefix, connector)
    else:
        colored_file_name = color_printer.get_colored_file_name(item.name)

        tree.append(f"{prefix}{connector} {colored_file_name}")


def get_connector(index, directory_items_length):
    last_item_index = directory_items_length - 1

    if index != last_item_index:
        return constants.TEE

    return constants.ELBOW


def generate_directory(tree, item, index, directory_items_length, prefix, connector):
    colored_root_directory = color_printer.get_colored_directory_name(item.name)

    tree.append(f"{prefix}{connector} {colored_root_directory}{os.sep}")

    if index != directory_items_length - 1:
        prefix += constants.PIPE_PREFIX
    else:
        prefix += constants.SPACE_PREFIX

    add_body(tree, item, prefix)
