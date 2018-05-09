import json
import os

def read_json(path):
    print("reading!!!", path)
    print("current dir", os.getcwd())
    with open(path) as f:
        data = json.load(f)
    return data

def validate_config(config):
    cols = ["interface_to_capture",
            "save_path",
            "hosts",
            "switches",
            "links",
            "commands"]

    for c in cols:
        if c not in config:
            return u"Please, add {} to config".format(c)
    return None