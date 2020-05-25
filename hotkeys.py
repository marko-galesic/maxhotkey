import json
import os
import xml.etree.ElementTree as ET
from configparser import ConfigParser

from macro_binder import MacroBinderCreator
from macro_writer import MacroWriter
from keyboard_map import KeyBoardMapCreator

import configure

config = configure.get_configuration(os.path.join("resources", "program_configuration.ini"))
APP_DATA_DIRECTORY = config['directories']['app_data_directory']
BASE_KBDX = config['directories']['base_kbdx']

configDocument = ET.parse(BASE_KBDX)

config = ConfigParser()
macro_writer = MacroWriter(
    "macros",
    os.path.join(APP_DATA_DIRECTORY, "usermacros"),
    os.path.join("resources", "macro_template"))
macro_binder = MacroBinderCreator(configDocument.getroot())
keyboard_map = KeyBoardMapCreator(
    os.path.join("resources", "keyboard-layout_blank.png"),
    os.path.join("resources", "keys.cfg"),
    os.path.join("resources", "arial.ttf")
)

hotkey_config = json.load(open(os.path.join("resources", "config.json")))

for keyboard_key in hotkey_config.keys():
    for key_combo in ["key", "shift", "ctrl", "alt", "shift-alt", "ctrl-alt"]:
        if key_combo in hotkey_config[keyboard_key].keys():
            macro_binder.bind(keyboard_key, key_combo)
            macro_name = hotkey_config[keyboard_key][key_combo]["macro"]["name"]
            macro_writer.write(hotkey_config[keyboard_key][key_combo]["macro"])

            if keyboard_key.lower() in keyboard_map.get_defined_keys():
                keyboard_map.add(keyboard_key, macro_name)

keyboard_map.save()
configDocument.write(os.path.join(APP_DATA_DIRECTORY, "en-US", "UI", "awesome.kbdx"))

