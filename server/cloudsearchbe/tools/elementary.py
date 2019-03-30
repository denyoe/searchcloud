import json


def read_from_file(path):
    file = open(path)
    return json.load(file)


def find_keywords(text):
    """Totally ignores the request since we're not focusing on this function.
    => Sends a dummy stuff
    """
    return ["dummy1", "dummy2"]