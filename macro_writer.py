import file_util
import sys

from os import path


class MacroWriter:

    def __init__(self,
                 macros_directory,
                 max_macros_directory,
                 macro_template_file,
                 if_statement=path.join("resources", "if_statement")):
        self.if_statement = file_util.file_as_string(if_statement)
        self.context_cache = {}
        self.macros_directory = macros_directory
        self.max_macros_directory = max_macros_directory
        self.macro_template = file_util.file_as_string(macro_template_file)

    def get_context(self, context):
        if context not in self.context_cache:
            self.context_cache[context] = file_util.file_as_string(path.join("resources", context))

        return self.context_cache[context]

    def generate_macro_body(self, macro):
        macro_name = macro["name"]
        macro_body = file_util.file_as_string(path.join(self.macros_directory, macro_name))

        if 'context' not in macro.keys():
            return macro_body

        context = macro["context"]
        if type(context) == str:
            context = self.get_context(context)
        if type(context) == list:
            contexts = []
            for c in context:
                contexts.append(self.get_context(c))
            context = ' and '.join(contexts)

        return self.if_statement.replace("${boolean}", context).replace("${statement}", macro_body)

    def write(self, macro):
        name = macro['name']
        body = self.generate_macro_body(macro)

        filename = "DragAndDrop-" + name + ".mcr"

        macro = self.macro_template.replace("body", body).replace("hot_key", name)

        if not path.exists(self.max_macros_directory):
            raise NotADirectoryError

        try:
            with open(path.join(self.max_macros_directory, filename), "w") as macro_file:
                for line in macro.split('\n'):
                    macro_file.write(line + '\n')
        except PermissionError:
            print("Insufficient permissions to write " + path.join(self.max_macros_directory, filename))
            sys.exit()