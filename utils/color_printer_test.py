import unittest
from unittest import mock

import color_printer
from colorama import Fore


class TestColorPrinter(unittest.TestCase):
    @mock.patch("colorama.init")
    def test_init_with_auto_reset_calls_init(self, mocked_init):
        color_printer.init_with_auto_reset()
        mocked_init.assert_called_with(autoreset=True)

    def test_get_colored_file_name(self):
        file_name = "test.txt"
        actual_result = color_printer.get_colored_file_name(file_name)
        expected_result = f"{Fore.BLUE}{file_name}"

        assert actual_result == expected_result

    def test_get_colored_directory_name(self):
        directory_name = "test"
        actual_result = color_printer.get_colored_directory_name(directory_name)
        expected_result = f"{Fore.MAGENTA}{directory_name}{Fore.RESET}"

        assert actual_result == expected_result


if __name__ == "__main__":
    unittest.main()
