import unittest
import file_util

from unittest.mock import Mock
from macro_writer import MacroWriter
from os import path


class MacroWriterTest(unittest.TestCase):

    def test_macros_directory_doesnt_exist(self):
        file_util.file_as_string = Mock(return_value='')
        macro_writer = MacroWriter('dummy_directory', 'dummy_template')

        with self.assertRaises(NotADirectoryError):
            macro_writer.write('red', 'herring')

    def test_macro_write(self):
        macro_writer = MacroWriter('./', '../macro_template')
        macro_writer.write('macro', '1 2 3')

        self.assertTrue(path.exists('./DragAndDrop-macro.mcr'), 'macro file should be created')
        self.assertEqual(
            file_util.file_as_string('macro_test'),
            file_util.file_as_string('DragAndDrop-macro.mcr')
        )

