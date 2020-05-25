import xml.etree.ElementTree as ET

pattern_to_fvirt_value = {
    "Ctrl": "11",
    "Alt": "19",
    "CtrlShift": "15",
    "Shift": "7",
    "ShiftAlt": "23",
    "CtrlAlt": "27"
}


class MacroBinderCreator:

    def __init__(self, root):
        self.root = root

    def bind(self, keyboard_key, key_combo, remove_existing_bindings=True):
        script_name = self.get_script_name(key_combo, keyboard_key)
        key = keyboard_key[len(keyboard_key) - 1] if "no" in keyboard_key else keyboard_key
        pattern = self.get_capitalized_key_combo_pattern(key_combo)

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

            for child in self.root:
                if child.attrib['fVirt'] == fvirt_value and child.attrib['accleleratorKey'] == ascii_value_of_key:
                    remove_these.append(child)

            for child in remove_these:
                self.root.remove(child)

        self.root.append(new_node)

    def get_capitalized_key_combo_pattern(self, key_combo):
        return ''.join([h.capitalize() for h in key_combo.split('-')])

    def get_script_name(self, key_combo, key):
        if key_combo != 'key':
            return self.get_capitalized_key_combo_pattern(key_combo) + key.capitalize()
        else:
            return key.capitalize()
