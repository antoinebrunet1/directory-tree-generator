import colorama
from colorama import Fore


def init_with_auto_reset():
    colorama.init(autoreset=True)


def get_colored_file_name(file_name):
    return f"{Fore.BLUE}{file_name}"


def get_colored_directory_name(directory_name):
    return f"{Fore.MAGENTA}{directory_name}{Fore.RESET}"
