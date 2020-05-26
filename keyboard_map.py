"""
Contains KeyBoardMapCreator
"""
from configparser import ConfigParser
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class KeyBoardMapCreator:
    """
    Creates keyboard hotkey map image
    """

    def __init__(self, keyboard_map_image, key_locations, font):
        self.config = ConfigParser()
        self.config.read(key_locations)
        self.locations = {}
        self.initialize_coordinates()

        self.keyboard_img = Image.open(keyboard_map_image)
        self.keyboard_reference = ImageDraw.Draw(self.keyboard_img)
        self.font = ImageFont.truetype(font, size=20)
        legend = ImageFont.truetype(font, size=100)

        self.keyboard_reference.rectangle([(1950, 450), (2600, 1500)], fill=(125, 125, 125))
        self.keyboard_reference.text((2000, 500), "SHIFT", fill=(227, 47, 47), font=legend)
        self.keyboard_reference.text((2000, 700), "CTRL", fill=(227, 47, 47), font=legend)
        self.keyboard_reference.text((2000, 900), "ALT", fill=(227, 47, 47), font=legend)
        self.keyboard_reference.text((2000, 1100), "SHIFT+ALT", fill=(227, 47, 47), font=legend)
        self.keyboard_reference.text((2000, 1300), "CTRL+ALT", fill=(227, 47, 47), font=legend)

    def get_defined_keys(self):
        """ Return keys defined in location config file """
        return self.locations.keys()

    def initialize_coordinates(self):
        """ Initialize locations dictionary with initial keyboard key coordinates for macros """
        for key in self.config['locations'].keys():
            self.locations[key] = [int(x) for x in self.config['locations'][key].split(',')]

    def next_coordinate(self, key):
        """ Get the next keyboard map macro coordinate """
        coordinate = self.locations[key]
        self.locations[key][1] += 25
        return coordinate

    def add(self, key, text):
        """ Add macro for key to keyboard map """
        coordinate = self.next_coordinate(key)
        self.keyboard_reference.text(coordinate, text, fill=(0, 0, 0), font=self.font)

    def save(self):
        """ Save keyboard map """
        self.keyboard_img.save('keyboard-layout.png')
