import unittest
from unittest.mock import patch
import configure
import os
from os import path


class ProgramConfigurationTest(unittest.TestCase):

    @patch('builtins.input', side_effect=['C:\\', 'C:\\'])
    def test_configuration_not_present(self, mock):
        self.assertFalse(path.exists('dummy'), "dummy configuration shouldn't be present")
        config = configure.get_configuration('dummy')

        self.assertTrue(config['directories']['app_data_directory'], 'C:\\')
        self.assertTrue(config['directories']['base_kbdx'], 'C:\\')

        os.remove('dummy')

    def test_configuration_present(self):
        config = configure.get_configuration('resources/test_config.ini')

        self.assertTrue(config['directories']['app_data_directory'], 'C:\\')
        self.assertTrue(config['directories']['base_kbdx'], 'C:\\')
