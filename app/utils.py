import json
import os


def get_keys():
    with open(os.path.join(os.path.abspath("./"), "keys.json")) as file:
        keys_file = json.load(file)
        username = keys_file["username"]
        password = keys_file["password"]

    return username, password
