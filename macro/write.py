"""
Write macro function files
"""
from os import path
import sys
from macro.util import get_script_name
import file_util



class MacroWriter:
    """
    Generates macro function files based on macro function bodies in macros directory and context
    (e.g. selected object is an editable poly), if configured.
    """

    def __init__(self, macros_directory, max_macros_directory, resources_directory):
        self.if_statement = file_util.file_as_string(path.join(resources_directory, "if_statement"))
        self.context_cache = {}
        self.context_directory = resources_directory
        self.macros_directory = macros_directory
        self.max_macros_directory = max_macros_directory
        self.macro_template = \
            file_util.file_as_string(path.join(resources_directory, "macro_template"))

    def get_context(self, context):
        """
        Gets MAXScript defining a context from cache or first places MAXScript from file for
        a context into cache
        """
        if context not in self.context_cache:
            self.context_cache[context] = \
                file_util.file_as_string(path.join(self.context_directory, context))

        return self.context_cache[context]

    def generate_macro_body(self, macro):
        """
        Generates macro body with context, if configured
        """
        macro_name = macro["name"]
        macro_body = file_util.file_as_string(path.join(self.macros_directory, macro_name))

        if 'context' not in macro.keys():
            return macro_body

        macro_context = macro["context"]
        if isinstance(macro_context, str):
            macro_context = self.get_context(macro_context)
        if isinstance(macro_context, list):
            contexts = []
            for context in macro_context:
                contexts.append(self.get_context(context))
            macro_context = ' and '.join(contexts)

        return self.if_statement\
            .replace("${boolean}", macro_context)\
            .replace("${statement}", macro_body)

    def write(self, macro, key, key_combo):
        """ Write macro script for hotkey into 3DS MAX user macro directory """
        script_name = get_script_name(key_combo, key)
        body = self.generate_macro_body(macro)

        filename = "DragAndDrop-" + script_name + ".mcr"

        macro = self.macro_template.replace("body", body).replace("hot_key", script_name)

        if not path.exists(self.max_macros_directory):
            raise NotADirectoryError

        try:
            with open(path.join(self.max_macros_directory, filename), "w") as macro_file:
                for line in macro.split('\n'):
                    macro_file.write(line + '\n')
        except PermissionError:
            print("Insufficient permissions to write " +
                  path.join(self.max_macros_directory, filename))
            sys.exit()
