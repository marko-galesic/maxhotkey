import unittest

from keyboard_map import KeyBoardMapCreator
from os import path


class KeyBoardMapCreatorTest(unittest.TestCase):

    def test_add_multiple_hotkeys(self):
        keyboard_map_creator = KeyBoardMapCreator(
            path.join(path.pardir, "resources", "keyboard-layout_blank.png"),
            path.join("resources", "keys.cfg"),
            path.join(path.pardir, "resources", "AcariSans-Regular.ttf")
        )
        keyboard_map_creator.add("a", "my-macro")
        keyboard_map_creator.add("a", "my-other-macro")
        keyboard_map_creator.save()

        saved_images = open("keyboard-layout.png", "rb").read()
        test_image = open(path.join("resources", "keyboard-layout.png"), "rb").read()

        self.assertTrue(saved_images == test_image)


