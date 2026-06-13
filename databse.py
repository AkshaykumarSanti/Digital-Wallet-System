import json
import os


FILE = "data/users.json"


def load_data():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as file:
        return json.load(file)



def save_data(data):

    with open(FILE, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )