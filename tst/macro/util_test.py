import unittest
from macro.util import get_capitalized_key_combo_pattern, get_script_name


class UtilTest(unittest.TestCase):

    def test_get_capitalized_key_combo_pattern(self):
        self.assertEqual(get_capitalized_key_combo_pattern("ctrl-alt"), "CtrlAlt")

    def test_get_script_name(self):
        self.assertEqual(get_script_name("key", "a"), "A")