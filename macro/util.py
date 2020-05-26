"""
Macro creation utilities
"""

def get_capitalized_key_combo_pattern(key_combo):
    """ (e.g. ctrl-shift -> CtrlShift) """
    return ''.join([h.capitalize() for h in key_combo.split('-')])


def get_script_name(key_combo, key):
    """ (e.g. ctrl-shift, a -> CtrlShiftA, a -> A """
    if key_combo != 'key':
        return get_capitalized_key_combo_pattern(key_combo) + key.capitalize()
    return key.capitalize()
