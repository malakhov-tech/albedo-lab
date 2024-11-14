from Processing import read_intensity_by_pixel, read_intensity_by_length, read_intensity_by_length_multiple, albedos
import os
from matplotlib import pyplot as plt


def draw_brightness_by_pixels():
    files = os.listdir("Pictures")

    for file in files:
        orig = "Pictures/" + file
        save_file = "Brightnesses_by_pixel/" + file
        read_intensity_by_pixel(orig, save_file, ("лампа накаливания" if "nakal" in file else "ртутная лампа"), (
            "красная" if "red" in file else "синяя" if "blue" in file
            else "зелёная" if "green" in file else "жёлтая" if "yellow" in file else "белая"))


def draw_brightness_by_length():
    files = os.listdir("Pictures")

    for file in files:
        orig = "Pictures/" + file
        save_file = "Brightnesses_by_length/by_length_" + file
        read_intensity_by_length(orig, ("лампа накаливания" if "nakal" in file else "ртутная лампа"), (
            "красная" if "red" in file else "синяя" if "blue" in file
            else "зелёная" if "green" in file else "жёлтая" if "yellow" in file else "белая"))
        plt.savefig(save_file)


def draw_brightness_by_length_all():
    files = os.listdir("Pictures")

    origs = ["Pictures/" + file for file in files]
    save_files = ["Brightnesses_by_length/by_length_" + file for file in files]
    lamps = ["лампа накаливания" if "nakal" in file else "ртутная лампа" for file in files]
    surfaces = [
            "красная" if "red" in file else "синяя" if "blue" in file
            else "зелёная" if "green" in file else "жёлтая" if "yellow" in file else "белая" for file in files
    ]

    read_intensity_by_length_multiple(origs, lamps, surfaces)
    plt.savefig("Brightnesses_by_length/all.jpg")
    albedos(origs, lamps, surfaces)
    plt.savefig("Brightnesses_by_length/albedo.jpg")
