def file_as_string(file):
    content = ""
    with open(file) as f:
        for line in f:
            content += line
    return content
