import configparser
from os import path


def get_configuration(configuration_file):
    program_config = configparser.ConfigParser()

    if not path.exists(configuration_file):
        print("Initial setup")
        app_data_directory = \
            input("3DS Max AppData directory (e.g. C:/Users/DummyUser/AppData/Local/Autodesk/3dsMax/2018 - 64bit/ENU): ")
        while not path.exists(app_data_directory):
            app_data_directory = input("Invalid directory - please enter a 3DS Max AppData directory: ")
        base_kbdx_directory = input("Base KBDX directory (e.g. C:/MaxStartUI.kbdx): ")
        while not path.exists(base_kbdx_directory):
            base_kbdx_directory = input("Invalid directory - please enter a Base KBDX directory: ")

        program_config['directories'] = {
            'app_data_directory': app_data_directory,
            'base_kbdx': base_kbdx_directory
        }
        with open(configuration_file, 'w') as config:
            program_config.write(config)
    else:
        program_config.read(configuration_file)

    return program_config
