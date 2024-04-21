from utils import directory_tree_generator
import pathlib

directory = input("Enter directory: ")

try:
    directory_tree_generator.print_tree(pathlib.Path(directory))
except Exception as e:
    raise e
