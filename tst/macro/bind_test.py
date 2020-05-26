import unittest
import xml.etree.ElementTree as ET
from os import path

from macro.bind import MacroBinderCreator


class MacroBinderTest(unittest.TestCase):

    def setUp(self):
        self.macro_binder = MacroBinderCreator("./", path.join(path.pardir, "resources", "test_binding_template.kbdx"))

    def test_default_key_binding(self):
        self.macro_binder.bind("a", "key")
        self.assertBindingValid("A", "97", "3")

    def test_replace_key_binding(self):
        new_node = ET.Element('shortcut')

        new_node.attrib['actionID'] = "test-macro`DragAndDrop"
        new_node.attrib['accleleratorKey'] = "97"
        new_node.attrib['fVirt'] = "3"
        new_node.attrib['actionTableID'] = "647394"

        self.macro_binder.key_bindings.getroot().append(new_node)

        self.macro_binder.bind("a", "key")

        shortcut_count = sum(1 for _ in self.macro_binder.key_bindings.getiterator("shortcut"))
        self.assertTrue(shortcut_count, 1)
        self.assertBindingValid("A", "97", "3")

    def test_combo_key_binding(self):
        self.macro_binder.bind("a", "CtrlShift")
        self.assertBindingValid("CtrlShift", "97", "15")

    def assertBindingValid(self, script_name, key, fvirt):
        binding = self.macro_binder.key_bindings.getiterator("shortcut").pop()
        self.assertTrue(binding.attrib['actionID'], script_name + "`DragAndDrop")
        self.assertTrue(binding.attrib['accleleratorKey'], key)
        self.assertTrue(binding.attrib['fVirt'], fvirt)
        self.assertTrue(binding.attrib['actionTableID'], "647394")
