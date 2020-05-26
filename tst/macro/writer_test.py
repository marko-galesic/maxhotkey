import file_util
import unittest
import os

from os import path
from os.path import dirname
from macro.write import MacroWriter
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
        self.grandparent_directory = dirname(path.abspath(os.curdir))
        self.great_grandparent_directory = dirname(dirname(path.abspath(os.curdir)))
        self.macro_creator = MacroWriter(
            path.join(self.grandparent_directory, "resources"),
            path.join(self.grandparent_directory, "resources"),
            path.join(self.grandparent_directory, "resources"))

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
        macro_writer = MacroWriter('dummy_directory', 'dummy_directory', 'dummy_directory')

        with self.assertRaises(NotADirectoryError):
            macro_writer.write(default_macro, "a", "key")

    def test_macro_write(self):
        self.macro_creator.write(default_macro, "a", "key")

        self.assertTrue(
            path.exists(path.join(self.grandparent_directory, "resources", "DragAndDrop-A.mcr")),
            "macro file should be created")
        self.assertEqual(
            file_util.file_as_string(path.join(self.grandparent_directory, "resources", "macro_test")),
            file_util.file_as_string(path.join(self.grandparent_directory, "resources", "DragAndDrop-A.mcr"))
        )
