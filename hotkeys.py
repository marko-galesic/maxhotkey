import json
import xml.etree.ElementTree as ET
from configparser import ConfigParser

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

APP_DATA_DIRECTORY = 'C:/Users/CONRAD II/AppData/Local/Autodesk/3dsMax/2018 - 64bit/ENU'
BASE_KBDX = 'C:/Users/CONRAD II/Desktop/MaxStartUI.kbdx'

MACROS_DIRECTORY = APP_DATA_DIRECTORY + '/usermacros/'
FILE_PREFIX = 'DragAndDrop'

config = ConfigParser()

hotkey_config = json.load(open('config.json'))
config.read('keys.cfg')
keyboard_img = Image.open('keyboard-layout_blank.png')
keyboard_reference = ImageDraw.Draw(keyboard_img)
font = ImageFont.truetype("arial.ttf", size=20)
legend = ImageFont.truetype("arial.ttf", size=100)
tree = ET.parse(BASE_KBDX)
root = tree.getroot()


def add_binding(name, pattern, key):

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
    else:
        fvirt_value = '3'

    new_node.attrib['actionID'] = name + "`DragAndDrop"
    new_node.attrib['accleleratorKey'] = str(ord(key.upper()))
    new_node.attrib['fVirt'] = fvirt_value
    new_node.attrib['actionTableID'] = "647394"

    root.append(new_node)


def get_macro(file):
    macro = ""
    with open("macros/" + file) as f:
        for line in f:
            macro += line
    return macro


def get_context(file):
    macro = ""
    with open(file) as f:
        for line in f:
            macro += line
    return macro


def get_template(file):
    template = ""
    with open(file) as f:
        for line in f:
            template += line

    return template


def get_capitalized_hotkey_pattern(hotkey):
    return ''.join([h.capitalize() for h in hotkey.split('-')])


def get_script_name(hotkey, key):
    if hotkey != 'key':
        return get_capitalized_hotkey_pattern(hotkey) + key.capitalize()
    else:
        return key.capitalize()

MACRO_TEMPLATE = get_template('macro_template')

locations = {}

for key_location in config['locations'].keys():

    anchor = [int(x) for x in config['locations'][key_location].split(',')]

    key_locations = []
    for y in range(anchor[1], anchor[1] + 150, 25):
        key_locations.append([anchor[0], y])

    locations[key_location] = key_locations

script_name = ''

keyboard_reference.text((2000, 500), "SHIFT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 700), "CTRL", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 900), "ALT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 1100), "SHIFT+ALT", fill=(227, 47, 47), font=legend)
keyboard_reference.text((2000, 1300), "CTRL+ALT", fill=(227, 47, 47), font=legend)

for keyboard_key in hotkey_config.keys():
    for hot_key in ["key", "shift", "ctrl", "alt", "shift-alt", "ctrl-alt"]:
        if hot_key in hotkey_config[keyboard_key].keys():
            script_name = get_script_name(hot_key, keyboard_key)

            add_binding(script_name, get_capitalized_hotkey_pattern(hot_key), keyboard_key[len(keyboard_key) - 1])

            macro_name = hotkey_config[keyboard_key][hot_key]["macro"]["name"]

            macro = get_macro(hotkey_config[keyboard_key][hot_key]["macro"]["name"])
            if_statement = get_template("if_statement")

            macro_body = ""

            if 'context' in hotkey_config[keyboard_key][hot_key]["macro"].keys():
                context = hotkey_config[keyboard_key][hot_key]["macro"]["context"]
                if type(context) == str:
                    context = get_context(context)
                if type(context) == list:
                    for c in range(len(context)):
                        context[c] = get_context(context[c])
                    context = ' and '.join(context)

                if_statement = if_statement.replace("${boolean}", context)
                if_statement = if_statement.replace("${statement}", macro)

                macro_body = if_statement
            else:
                macro_body = macro

            macro_filename = "DragAndDrop-" + script_name + ".mcr"

            MACRO_TEMPLATE = get_template("macro_template").replace("body", macro_body).replace("hot_key", script_name)

            if keyboard_key.lower() in locations:
                location = locations[keyboard_key.lower()].pop(0)
                keyboard_reference.text((location[0], location[1]), macro_name, fill=(0, 0, 0), font=font)

            with open(MACROS_DIRECTORY + macro_filename, "w") as macro_file:

                for line in MACRO_TEMPLATE.split('\n'):
                    macro_file.write(line + '\n')

keyboard_img.save('keyboard-layout.png')
tree.write(APP_DATA_DIRECTORY + '/en-US/UI/awesome.kbdx')
