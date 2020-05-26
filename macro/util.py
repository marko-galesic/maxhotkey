def get_capitalized_key_combo_pattern(key_combo):
    return ''.join([h.capitalize() for h in key_combo.split('-')])


def get_script_name(key_combo, key):
    if key_combo != 'key':
        return get_capitalized_key_combo_pattern(key_combo) + key.capitalize()
    else:
        return key.capitalize()
