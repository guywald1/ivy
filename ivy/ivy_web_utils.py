import json

def cy_elements_to_json(elements):
    if hasattr(elements, 'cy_elements'):
        elements_str = repr(elements['cy_elements']['elements'])[1:-1]
    else:
        elements_str = repr(elements)
    return '{{ "elements": {} }}'.format(elements_str.replace("True", "true").replace("False", "false").replace("'", "\"").replace("None", "null"))