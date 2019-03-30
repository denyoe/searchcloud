import json


def read_from_file(path):
    file = open(path)
    return json.load(file)

