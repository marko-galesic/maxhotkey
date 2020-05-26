import configure
import json
import os

from keyboard_map import KeyBoardMapCreator
from macro.bind import MacroBinderCreator
from macro.write import MacroWriter

config = configure.get_configuration(os.path.join("resources", "program_configuration.ini"))
app_data_directory = config['directories']['app_data_directory']
base_kbdx = config['directories']['base_kbdx']

macro_writer = MacroWriter(
    "macros",
    os.path.join(app_data_directory, "usermacros"),
    "resources",
    os.path.join("resources", "macro_template"))
macro_binder = MacroBinderCreator(app_data_directory, base_kbdx)
keyboard_map = KeyBoardMapCreator(
    os.path.join("resources", "keyboard-layout_blank.png"),
    os.path.join("resources", "keys.cfg"),
    os.path.join("resources", "AcariSans-Regular.ttf"))

hotkey_config = json.load(open(os.path.join("resources", "config.json")))

for keyboard_key in hotkey_config.keys():
    for key_combo in ["key", "shift", "ctrl", "alt", "shift-alt", "ctrl-alt"]:
        if key_combo in hotkey_config[keyboard_key].keys():
            macro_binder.bind(keyboard_key, key_combo)
            macro_writer.write(hotkey_config[keyboard_key][key_combo]["macro"], keyboard_key, key_combo)

            if keyboard_key.lower() in keyboard_map.get_defined_keys():
                keyboard_map.add(keyboard_key, hotkey_config[keyboard_key][key_combo]["macro"]["name"])
            else:
                print("Warning: " + hotkey_config[keyboard_key][key_combo]["macro"]["name"] +
                      " is bound in 3DS Max, but not added to the keyboard map. " +
                      "Please add an entry for" + keyboard_key + " in " + os.path.join("resources", "keys.cfg") +
                      " for your macro to show on the map.")

keyboard_map.save()
macro_binder.save_key_bindings()

