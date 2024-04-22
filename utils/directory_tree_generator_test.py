import unittest
from unittest import mock
from unittest.mock import call

from colorama import Fore

import constants
import directory_tree_generator
import pathlib
import os


class DirectoryTreeGeneratorTest(unittest.TestCase):
    @mock.patch("builtins.print")
    @mock.patch("directory_tree_generator.make_tree")
    def test_print_tree_calls_make_tree_with_root_directory_with_correct_argument(self, mocked_make_tree, mocked_print):
        root_directory_name = "test"
        root_directory = pathlib.Path(root_directory_name)
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        file_name = "test.txt"
        colored_file_name = f"{Fore.BLUE}{file_name}"
        expected_tree = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
            f"{constants.ELBOW} {colored_file_name}"
        ]
        mocked_make_tree.return_value = expected_tree

        directory_tree_generator.print_tree(root_directory)
        mocked_make_tree.assert_called_with(root_directory)

    @mock.patch("builtins.print")
    @mock.patch("directory_tree_generator.make_tree")
    def test_print_tree_prints_every_line_of_tree(self, mocked_make_tree, mocked_print):
        root_directory_name = "test"
        root_directory = pathlib.Path(root_directory_name)
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        file_name = "test.txt"
        colored_file_name = f"{Fore.BLUE}{file_name}"
        expected_tree = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
            f"{constants.ELBOW} {colored_file_name}"
        ]
        mocked_make_tree.return_value = expected_tree
        calls = []

        for line in expected_tree:
            calls.append(call(line))

        directory_tree_generator.print_tree(root_directory)
        mocked_print.assert_has_calls(calls)

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("directory_tree_generator.add_root")
    @mock.patch("utils.color_printer.init_with_auto_reset")
    def test_make_tree_calls_init_with_auto_reset(self, mocked_init_with_auto_reset, mocked_add_root, mocked_add_body):
        root_directory = pathlib.Path("test")

        directory_tree_generator.make_tree(root_directory)
        mocked_init_with_auto_reset.assert_called()

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("directory_tree_generator.add_root")
    @mock.patch("utils.color_printer.init_with_auto_reset")
    def test_make_tree_calls_add_root_with_correct_argument(self, mocked_init_with_auto_reset, mocked_add_root,
                                                            mocked_add_body):
        root_directory = pathlib.Path("test")
        tree = []

        directory_tree_generator.make_tree(root_directory)
        mocked_add_root.assert_called_with(tree, root_directory)

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("directory_tree_generator.add_root")
    @mock.patch("utils.color_printer.init_with_auto_reset")
    def test_make_tree_calls_add_body_with_correct_argument(self, mocked_init_with_auto_reset, mocked_add_root,
                                                            mocked_add_body):
        root_directory = pathlib.Path("test")
        tree = []

        directory_tree_generator.make_tree(root_directory)
        mocked_add_body.assert_called_with(tree, root_directory)

    @mock.patch("utils.color_printer.get_colored_directory_name")
    def test_add_root_calls_get_colored_directory_name_with_correct_argument(self, mocked_get_colored_directory_name):
        tree = []
        root_directory = pathlib.Path("test")

        directory_tree_generator.add_root(tree, root_directory)
        mocked_get_colored_directory_name.assert_called_with(root_directory.name)

    def test_add_root_appends_correct_lines(self):
        root_directory = pathlib.Path("test")
        tree = []
        colored_root_directory = f"{Fore.MAGENTA}{root_directory.name}{Fore.RESET}"
        first_expected_appended_line = f"{colored_root_directory}{os.sep}"
        second_expected_appended_line = constants.PIPE

        directory_tree_generator.add_root(tree, root_directory)
        assert len(tree) == 2
        assert tree[0] == first_expected_appended_line
        assert tree[1] == second_expected_appended_line

    @mock.patch("directory_tree_generator.handle_item")
    @mock.patch("pathlib.Path.iterdir")
    def test_add_body_calls_handle_item_for_each_line_with_correct_parameters(self, mocked_iterdir, mocked_handle_item):
        first_file_name = "test1.txt"
        second_file_name = "test2.txt"
        mocked_iterdir_return_value = [
            pathlib.Path(first_file_name),
            pathlib.Path(second_file_name)
        ]
        mocked_iterdir.return_value = mocked_iterdir_return_value
        items_length = 2
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        tree_with_only_root_directory = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
        ]
        prefix = ""
        first_call = call(
            0,
            mocked_iterdir_return_value[0],
            items_length,
            tree_with_only_root_directory,
            prefix
        )
        second_call = call(
            1,
            mocked_iterdir_return_value[1],
            items_length,
            tree_with_only_root_directory,
            prefix
        )
        calls = [first_call, second_call]
        root_directory = pathlib.Path(root_directory_name)

        directory_tree_generator.add_body(tree_with_only_root_directory, root_directory)
        mocked_handle_item.assert_has_calls(calls)

    @mock.patch("directory_tree_generator.generate_directory")
    @mock.patch("pathlib.Path.is_dir", return_value=True)
    @mock.patch("directory_tree_generator.get_connector", return_value=constants.ELBOW)
    def test_handle_item_calls_generate_directory_with_correct_parameters_for_directory(self, mocked_get_connector,
                                                                                        mocked_is_dir,
                                                                                        mocked_generate_directory):
        sub_folder_name = "test-sub-folder"
        item = pathlib.Path(sub_folder_name)
        index = 0
        items_length = 1
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        tree_with_only_root_directory = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
        ]
        prefix = ""
        connector = constants.ELBOW

        directory_tree_generator.handle_item(index, item, items_length, tree_with_only_root_directory, prefix)
        mocked_generate_directory.assert_called_with(tree_with_only_root_directory, item, index, items_length, prefix,
                                                     connector)

    @mock.patch("utils.color_printer.get_colored_file_name")
    @mock.patch("pathlib.Path.is_dir", return_value=False)
    @mock.patch("directory_tree_generator.get_connector", return_value=constants.ELBOW)
    def test_handle_item_calls_get_colored_file_name_with_correct_parameter_for_file(self, mocked_get_connector,
                                                                                     mocked_is_dir,
                                                                                     mocked_get_colored_file_name):
        file_name = "test1.txt"
        index = 0
        item = pathlib.Path(file_name)
        items_length = 1
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        tree_with_only_root_directory = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
        ]
        prefix = ""

        directory_tree_generator.handle_item(index, item, items_length, tree_with_only_root_directory, prefix)
        mocked_get_colored_file_name.assert_called_with(file_name)

    @mock.patch("pathlib.Path.is_dir", return_value=False)
    @mock.patch("directory_tree_generator.get_connector", return_value=constants.ELBOW)
    def test_handle_item_appends_correct_line_for_file(self, mocked_get_connector, mocked_is_dir):
        file_name = "test1.txt"
        index = 0
        item = pathlib.Path(file_name)
        items_length = 1
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        first_line = f"{colored_root_directory_name}{os.sep}"
        second_line = constants.PIPE
        tree_with_only_root_directory = [
            first_line,
            second_line,
        ]
        prefix = ""
        colored_file_name = f"{Fore.BLUE}{file_name}"
        expected_appended_line = f"{prefix}{constants.ELBOW} {colored_file_name}"

        directory_tree_generator.handle_item(index, item, items_length, tree_with_only_root_directory, prefix)
        assert len(tree_with_only_root_directory) == 3
        assert tree_with_only_root_directory[0] == first_line
        assert tree_with_only_root_directory[1] == second_line
        assert tree_with_only_root_directory[2] == expected_appended_line

    def test_get_connector_returns_tee_if_index_is_not_last_one(self):
        directory_items_length = 2
        index = 0
        actual_connector = directory_tree_generator.get_connector(index, directory_items_length)
        expected_connector = constants.TEE

        assert actual_connector == expected_connector

    def test_get_connector_returns_elbow_if_index_is_last_one(self):
        directory_items_length = 2
        index = directory_items_length - 1
        actual_connector = directory_tree_generator.get_connector(index, directory_items_length)
        expected_connector = constants.ELBOW

        assert actual_connector == expected_connector

    def test_get_connector_raises_value_error_when_index_is_greater_than_last_index(self):
        directory_items_length = 2
        index = directory_items_length

        self.assertRaises(ValueError, directory_tree_generator.get_connector, index, directory_items_length)

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("utils.color_printer.get_colored_directory_name")
    def test_generate_directory_calls_get_colored_directory_name_with_correct_argument(self,
                                                                                       mocked_get_colored_directory_name,
                                                                                       mocked_add_body):
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        tree_with_only_root_directory = [
            f"{colored_root_directory_name}{os.sep}",
            constants.PIPE,
        ]
        sub_folder_name = "sub-folder"
        item = pathlib.Path(sub_folder_name)
        index = 0
        directory_items_length = 1
        prefix = ""
        connector = constants.ELBOW

        directory_tree_generator.generate_directory(tree_with_only_root_directory, item, index, directory_items_length,
                                                    prefix, connector)
        mocked_get_colored_directory_name.assert_called_with(sub_folder_name)

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("utils.color_printer.get_colored_directory_name")
    def test_generate_directory_appends_line_for_current_folder(self, mocked_get_colored_directory_name,
                                                                mocked_add_body):
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        first_line = f"{colored_root_directory_name}{os.sep}"
        second_line = constants.PIPE
        tree_with_only_root_directory = [
            first_line,
            second_line,
        ]
        sub_folder_name = "sub-folder"
        item = pathlib.Path(sub_folder_name)
        index = 0
        directory_items_length = 1
        prefix = ""
        connector = constants.ELBOW
        colored_sub_folder = f"{Fore.MAGENTA} {sub_folder_name}{Fore.RESET}"
        mocked_get_colored_directory_name.return_value = colored_sub_folder
        expected_appended_line = f"{prefix}{connector} {colored_sub_folder}{os.sep}"

        directory_tree_generator.generate_directory(tree_with_only_root_directory, item, index, directory_items_length,
                                                    prefix, connector)
        assert len(tree_with_only_root_directory) == 3
        assert tree_with_only_root_directory[0] == first_line
        assert tree_with_only_root_directory[1] == second_line
        assert tree_with_only_root_directory[2] == expected_appended_line

    @mock.patch("directory_tree_generator.add_body")
    @mock.patch("utils.color_printer.get_colored_directory_name")
    def test_generate_directory_calls_add_body_with_correct_arguments(self, mocked_get_colored_directory_name,
                                                                mocked_add_body):
        root_directory_name = "test"
        colored_root_directory_name = f"{Fore.MAGENTA}{root_directory_name}{Fore.RESET}"
        first_line = f"{colored_root_directory_name}{os.sep}"
        second_line = constants.PIPE
        tree_with_only_root_directory = [
            first_line,
            second_line,
        ]
        sub_folder_name = "sub-folder"
        item = pathlib.Path(sub_folder_name)
        index = 0
        directory_items_length = 1
        prefix = ""
        connector = constants.ELBOW
        colored_sub_folder = f"{Fore.MAGENTA} {sub_folder_name}{Fore.RESET}"
        mocked_get_colored_directory_name.return_value = colored_sub_folder
        expected_appended_line = f"{prefix}{connector} {colored_sub_folder}{os.sep}"
        expected_tree = [
            first_line,
            second_line,
            expected_appended_line
        ]
        expected_prefix = f"{prefix}{constants.SPACE_PREFIX}"

        directory_tree_generator.generate_directory(tree_with_only_root_directory, item, index, directory_items_length,
                                                    prefix, connector)

        mocked_add_body.assert_called_with(expected_tree, item, expected_prefix)


if __name__ == "__main__":
    unittest.main()
