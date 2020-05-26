"""
See README.md
"""
import json
import os
import configure

from keyboard_map import KeyBoardMapCreator
from macro.bind import MacroBinderCreator
from macro.write import MacroWriter

PROGRAM_CONFIG = configure.get_configuration(os.path.join("resources", "program_configuration.ini"))
APP_DATA_DIRECTORY = PROGRAM_CONFIG['directories']['app_data_directory']
BASE_KBDX = PROGRAM_CONFIG['directories']['base_kbdx']

MACRO_WRTIER = MacroWriter(
    "macros",
    os.path.join(APP_DATA_DIRECTORY, "usermacros"),
    "resources")
MACRO_BINDER = MacroBinderCreator(APP_DATA_DIRECTORY, BASE_KBDX)
KEYBOARD_MAP = KeyBoardMapCreator(
    os.path.join("resources", "keyboard-layout_blank.png"),
    os.path.join("resources", "keys.cfg"),
    os.path.join("resources", "AcariSans-Regular.ttf"))

HOTKEY_CONFIG = json.load(open(os.path.join("resources", "config.json")))

for keyboard_key in HOTKEY_CONFIG.keys():
    for key_combo in ["key", "shift", "ctrl", "alt", "shift-alt", "ctrl-alt"]:
        if key_combo in HOTKEY_CONFIG[keyboard_key].keys():
            MACRO_BINDER.bind(keyboard_key, key_combo)
            MACRO_WRTIER.write(HOTKEY_CONFIG[keyboard_key][key_combo]["macro"],
                               keyboard_key, key_combo)

            if keyboard_key.lower() in KEYBOARD_MAP.get_defined_keys():
                KEYBOARD_MAP.add(keyboard_key,
                                 HOTKEY_CONFIG[keyboard_key][key_combo]["macro"]["name"])
            else:
                print("Warning: " + HOTKEY_CONFIG[keyboard_key][key_combo]["macro"]["name"] +
                      " is bound in 3DS Max, but not added to the keyboard map. " +
                      "Please add an entry for" + keyboard_key + " in " +
                      os.path.join("resources", "keys.cfg") + " for your macro to show on the map.")

KEYBOARD_MAP.save()
MACRO_BINDER.save_key_bindings()
