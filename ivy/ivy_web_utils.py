import json

def cy_elements_to_json(elements):
    return repr(elements).replace("True", "true").replace("False", "false").replace("'", "\"").replace("None", "null")