import json


class File:
    @staticmethod
    def write(file, value):
        if type(value) != str:
            value = json.dumps(value)
        with open(file, "w") as file:
            return file.write(value)

    @staticmethod
    def read(file):
        with open(file, "r") as file:
            return file.read()
