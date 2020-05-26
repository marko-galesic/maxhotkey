import xml.etree.ElementTree as ET

from macro.util import get_script_name, get_capitalized_key_combo_pattern
from os import path

pattern_to_fvirt_value = {
    "Ctrl": "11",
    "Alt": "19",
    "CtrlShift": "15",
    "Shift": "7",
    "ShiftAlt": "23",
    "CtrlAlt": "27"
}

"""
Using a base KBDX (https://tinyurl.com/yayotz4a) file, creates & saves 3DS Max key bindings to 'awesome.kbdx', which
gets stored in the 3DS Max UI directory.

Appends new key bindings and overwrites existing key bindings.
"""
class MacroBinderCreator:

    def __init__(self, app_data_directory, base_kbdx):
        self.app_data_directory = app_data_directory
        self.key_bindings = ET.parse(base_kbdx)

    def bind(self, keyboard_key, key_combo, remove_existing_bindings=True):
        script_name = get_script_name(key_combo, keyboard_key)
        key = keyboard_key[len(keyboard_key) - 1] if "no" in keyboard_key else keyboard_key
        pattern = get_capitalized_key_combo_pattern(key_combo)

        new_node = ET.Element('shortcut')

        fvirt_value = "3"
        if pattern in pattern_to_fvirt_value:
            fvirt_value = pattern_to_fvirt_value[pattern]

        ascii_value_of_key = str(ord(key.upper())) if "SPACE" != key.upper() else "32"

        new_node.attrib['actionID'] = script_name + "`DragAndDrop"
        new_node.attrib['accleleratorKey'] = ascii_value_of_key
        new_node.attrib['fVirt'] = fvirt_value
        new_node.attrib['actionTableID'] = "647394"

        if remove_existing_bindings:
            remove_these = []

            root = self.key_bindings.getroot()

            for child in root:
                if child.attrib['fVirt'] == fvirt_value and child.attrib['accleleratorKey'] == ascii_value_of_key:
                    remove_these.append(child)

            for child in remove_these:
                root.remove(child)

        self.key_bindings.getroot().append(new_node)

    def save_key_bindings(self):
        self.key_bindings.write(path.join(self.app_data_directory, "en-US", "UI", "awesome.kbdx"))
