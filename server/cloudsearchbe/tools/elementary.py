import json


def read_from_file(path):
    file = open(path)
    return json.load(file)


def find_keywords(text):
    return ["dummy1", "dummy2"]