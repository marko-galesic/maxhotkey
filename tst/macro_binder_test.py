import unittest
import xml.etree.ElementTree as ET

from macro_binder import MacroBinderCreator


class MacroBinderTest(unittest.TestCase):

    def setUp(self):
        self.config = ET.parse("resources/test_binding_template.kbdx")
        self.macro_binder = MacroBinderCreator(self.config.getroot())

    def test_default_key_binding(self):
        self.macro_binder.bind("test-macro", "key", "a")
        self.assertBindingValid("test-macro", "97", "3")

    def test_replace_key_binding(self):
        new_node = ET.Element('shortcut')

        new_node.attrib['actionID'] = "test-macro`DragAndDrop"
        new_node.attrib['accleleratorKey'] = "97"
        new_node.attrib['fVirt'] = "3"
        new_node.attrib['actionTableID'] = "647394"

        self.config.getroot().append(new_node)

        self.macro_binder.bind("test-macro", "key", "a")

        shortcut_count = sum(1 for _ in self.config.getiterator("shortcut"))
        self.assertTrue(shortcut_count, 1)
        self.assertBindingValid("test-macro", "97", "3")

    def test_combo_key_binding(self):
        self.macro_binder.bind("test-macro", "CtrlShift", "a")
        self.assertBindingValid("test-macro", "97", "15")

    def assertBindingValid(self, script_name, key, fvirt):
        binding = self.config.getiterator("shortcut").pop()
        self.assertTrue(binding.attrib['actionID'], script_name + "`DragAndDrop")
        self.assertTrue(binding.attrib['accleleratorKey'], key)
        self.assertTrue(binding.attrib['fVirt'], fvirt)
        self.assertTrue(binding.attrib['actionTableID'], "647394")
