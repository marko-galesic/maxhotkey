import file_util
from os import path


class MacroWriter:
    def __init__(self, macros_directory, macro_template_file):
        self.macros_directory = macros_directory
        self.macro_template = file_util.file_as_string(macro_template_file)

    def write(self, name, body):
        filename = "DragAndDrop-" + name + ".mcr"

        macro = self.macro_template.replace("body", body).replace("hot_key", name)

        if not path.exists(self.macros_directory):
            raise NotADirectoryError

        with open(self.macros_directory + filename, "w") as macro_file:
            for line in macro.split('\n'):
                macro_file.write(line + '\n')