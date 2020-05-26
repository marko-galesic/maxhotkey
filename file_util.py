"""
File utility functions
"""
import sys


def file_as_string(file_name):
    """
    Creates a string from file contents
    :return: file content as string
    """

    content = ""

    try:
        with open(file_name, 'r') as file:
            for line in file:
                content += line
        return content
    except PermissionError:
        print("Insufficient permissions to open " + file_name)
        sys.exit()
