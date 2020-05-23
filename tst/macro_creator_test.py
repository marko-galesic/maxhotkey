import file_util
import unittest

from macro_writer import MacroWriter
from os import path
from unittest.mock import Mock

default_macro = {'name': "test-macro"}
macro_with_a_context = {
    'name': 'test-macro',
    'context': 'test-context'
}
macro_with_multiple_contexts = {
    'name': 'test-macro',
    'context': ['test-context', 'test-context2']
}


class MacroWriterTest(unittest.TestCase):

    def setUp(self):
        self.macro_creator = MacroWriter('./', './', '../macro_template', '../if_statement')

    def test_create_default_macro(self):
        macro_body = self.macro_creator.generate_macro_body(default_macro)

        self.assertEqual('foo bar', macro_body)

    def test_create_macro_for_single_context(self):
        macro_body = self.macro_creator.generate_macro_body(macro_with_a_context)

        self.assertEqual('if some context then (\nfoo bar\n)', macro_body)

    def test_create_macro_for_multiple_contexts(self):
        macro_body = self.macro_creator.generate_macro_body(macro_with_multiple_contexts)

        self.assertEqual('if some context and another context then (\nfoo bar\n)', macro_body)

    def test_macros_directory_doesnt_exist(self):
        file_util.file_as_string = Mock(return_value='')
        macro_writer = MacroWriter('dummy_directory', 'dummy_template', '../if_statement')

        with self.assertRaises(NotADirectoryError):
            macro_writer.write(default_macro)

    def test_macro_write(self):
        self.macro_creator.write(default_macro)

        self.assertTrue(path.exists('./DragAndDrop-macro.mcr'), 'macro file should be created')
        self.assertEqual(
            file_util.file_as_string('macro_test'),
            file_util.file_as_string('DragAndDrop-macro.mcr')
        )