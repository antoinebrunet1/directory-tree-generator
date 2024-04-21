import unittest
import color_printer
from colorama import Fore


class TestColorPrinter(unittest.TestCase):
    def test_get_colored_file_name(self):
        file_name = "test.txt"
        actual_result = color_printer.get_colored_file_name(file_name)
        expected_result = f"{Fore.BLUE}{file_name}"

        self.assertEqual(actual_result, expected_result)

    def test_get_colored_directory_name(self):
        directory_name = "test"
        actual_result = color_printer.get_colored_directory_name(directory_name)
        expected_result = f"{Fore.MAGENTA}{directory_name}{Fore.RESET}"

        self.assertEqual(actual_result, expected_result)
