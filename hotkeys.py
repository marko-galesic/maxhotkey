import configure
import json
import os
import sys
import xml.etree.ElementTree as ET

from configparser import ConfigParser
from macro_writer import MacroWriter
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


config = configure.get_configuration(os.path.join("resources", "program_configuration.ini"))
APP_DATA_DIRECTORY = config['directories']['app_data_directory']
BASE_KBDX = config['directories']['base_kbdx']

config = ConfigParser()
macro_writer = MacroWriter(
    "macros",
    os.path.join(APP_DATA_DIRECTORY, "usermacros"),
    os.path.join("resources", "macro_template"))

hotkey_config = json.load(open(os.path.join("resources", "config.json")))
config.read(os.path.join("resources", "keys.cfg"))
keyboard_img = Image.open(os.path.join("resources", "keyboard-layout_blank.png"))
keyboard_reference = ImageDraw.Draw(keyboard_img)
font = ImageFont.truetype(os.path.join("resources", "arial.ttf"), size=20)
legend = ImageFont.truetype(os.path.join("resources", "arial.ttf"), size=100)
tree = ET.parse(BASE_KBDX)
root = tree.getroot()


def bind(name, pattern, key, remove_existing_bindings=True):

    new_node = ET.Element('shortcut')

    if pattern == 'Ctrl':
        fvirt_value = "11"
    elif pattern == 'Alt':
        fvirt_value = '19'
    elif pattern == 'CtrlShift':
        fvirt_value = '15'
    elif pattern == 'Shift':
        fvirt_value = '7'
    elif pattern == 'ShiftAlt':
        fvirt_value = '23'
    elif pattern == 'CtrlAlt':
        fvirt_value = '27'
    else:
        fvirt_value = '3'

    ascii_value_of_key = str(ord(key.upper())) if "SPACE" != key.upper() else "32"

    new_node.attrib['actionID'] = name + "`DragAndDrop"
    new_node.attrib['accleleratorKey'] = ascii_value_of_key
    new_node.attrib['fVirt'] = fvirt_value
    new_node.attrib['actionTableID'] = "647394"

    if remove_existing_bindings:
        remove_these = []

        for child in root:
            if child.attrib['fVirt'] == fvirt_value and child.attrib['accleleratorKey'] == ascii_value_of_key:
                remove_these.append(child)

        for child in remove_these:
            root.remove(child)

    root.append(new_node)


def get_capitalized_hotkey_pattern(hotkey):
    return ''.join([h.capitalize() for h in hotkey.split('-')])


def get_script_name(hotkey, key):
    if hotkey != 'key':
        return get_capitalized_hotkey_pattern(hotkey) + key.capitalize()
    else:
        return key.capitalize()

locations = {}

for key_location in config['locations'].keys():

    anchor = [int(x) for x in config['locations'][key_location].split(',')]

    key_locations = []
    for y in range(anchor[1], anchor[1] + 150, 25):
        key_locations.append([anchor[0], y])

    locations[key_location] = key_locations

script_name = ''

keyboard_reference.rectangle([(1950, 450), (2600,1500)], fill=(125,125,125))
keyboard_reference.text((2000, 500), "SHIFT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 700), "CTRL", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 900), "ALT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 1100), "SHIFT+ALT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 1300), "CTRL+ALT", fill=(227, 47, 47), font=legend)

for keyboard_key in hotkey_config.keys():
    for hot_key in ["key", "shift", "ctrl", "alt", "shift-alt", "ctrl-alt"]:
        current_location = locations[keyboard_key.lower()].pop(0)
        if hot_key in hotkey_config[keyboard_key].keys():
            script_name = get_script_name(hot_key, keyboard_key)

            bind(script_name, get_capitalized_hotkey_pattern(hot_key), keyboard_key[len(keyboard_key) - 1] if "No" in keyboard_key else keyboard_key)

            macro_name = hotkey_config[keyboard_key][hot_key]["macro"]["name"]
            macro_writer.write(hotkey_config[keyboard_key][hot_key]["macro"])

            if keyboard_key.lower() in locations:
                keyboard_reference.text(
                    (current_location[0], current_location[1]), macro_name, fill=(0, 0, 0), font=font)

keyboard_img.save('keyboard-layout.png')
tree.write(APP_DATA_DIRECTORY + '/en-US/UI/awesome.kbdx')

