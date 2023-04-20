import argparse
import subprocess
import sys


def check_sanitizers_in_elf_file(file_path: str) -> dict[str, bool]:
    """
    Check if the ELF file contains sanitizers:
    AddressSanitizer, ThreadSanitizer, MemorySanitizer.

    :param file_path: path to the ELF file
    :return: dictionary with name of sanitizer as key and bool value
             of its presence
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


def main():
    file_path = input('Specify the path to the required ELF file: ')
    print(check_sanitizers_in_elf_file(file_path))


if __name__ == '__main__':
    main()
