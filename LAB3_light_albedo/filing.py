import os

files = os.listdir("Pictures")


def get_pictures():
    return ["Pictures/" + file for file in files]

