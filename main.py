import sys
import os

import subprocess


welcome_text = 'To check an elf or .so file for sanitizers, ' \
               'enter the absolute path to the required file.' \
               ' Enter "exit" if you want to stop checking files.'
request_path_text = 'Specify the path to the required ELF file or enter "exit": '


def check_sanitizers_in_elf_file(file_path: str) -> dict[str, bool]:
    """
    Check if the ELF file contains sanitizers:
    AddressSanitizer, ThreadSanitizer, MemorySanitizer.

    :param file_path: path to the ELF file
    :return: dictionary with name of sanitizer as key and
             bool value of its presence
    """
    try:
        output = subprocess.check_output(
            ['readelf', '-s', file_path],
            universal_newlines=True
        )
    except FileNotFoundError:
        print(
            'Make sure, that readelf is installed on your system and added to PATH'
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f'Error while executing readelf: {e}')
        sys.exit(1)

    return {
        'AddressSanitizer': '__asan_init' in output,
        'ThreadSanitizer': '__tsan_init' in output,
        'MemorySanitizer': '__msan_init' in output,
    }


def pretty_print_for_sanitizers(sanitizers_dict: dict[str, bool]) -> None:
    """
    Print the result of checking for sanitizers in a pretty way.

    :param sanitizers_dict: dictionary with name of sanitizer as key and
           bool value of its presence
    """
    for sanitizer_name, is_present in sanitizers_dict.items():
        print(f'Sanitizer {sanitizer_name}: '
              f'{is_present and "set" or "not set"} up for this file.')

    print()


def main():
    print(welcome_text)

    exit_or_file_path_command = input(request_path_text)

    while exit_or_file_path_command.lower() != 'exit':
        if os.path.exists(exit_or_file_path_command) and os.path.isfile(exit_or_file_path_command):

            pretty_print_for_sanitizers(
                check_sanitizers_in_elf_file(exit_or_file_path_command)
            )
        else:
            print('Path to file is incorrect. Try again.')
        exit_or_file_path_command = input(request_path_text)


if __name__ == '__main__':
    main()
