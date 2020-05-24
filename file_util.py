import sys


def file_as_string(file):
    content = ""

    try:
        with open(file, 'r') as f:
            for line in f:
                content += line
        return content
    except PermissionError:
        print("Insufficient permissions to open " + file)
        sys.exit()
