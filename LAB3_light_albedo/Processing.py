import numpy as np
import matplotlib.pyplot as plt
import imageio
from cycler import cycler
from scipy.optimize import curve_fit
from matplotlib.ticker import MultipleLocator


X_LEFT, X_RIGHT = 870, 1180

COLORS = {"белая": "white",
          "красная": "red",
          "жёлтая": "yellow",
          "синяя": "blue",
          "зелёная": "green"}


def get_bcg(photo):
    return photo[500:700, X_LEFT:X_RIGHT, 0:3]


def get_cut(photo):
    return photo[575:625, X_LEFT:X_RIGHT, 0:3]


def get_intensity_map(photo_name):
    photo = imageio.imread(photo_name)

    cut = get_cut(photo)
    rgb = np.mean(cut, axis=(0,))
    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]
    return rgb, luma


def read_intensity_by_pixel(photo_name, plot_name, lamp, surface):
    photo = imageio.imread(photo_name)
    background = get_bcg(photo)

    rgb, luma = get_intensity_map(photo_name)

    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

    fig = plt.figure(figsize=(10, 5), dpi=300)

    plt.title('Интенсивность отражённого излучения\n' + '{} / {} поверхность'.format(lamp, surface))
    plt.xlabel('Относительный номер пикселя')
    plt.ylabel('Яркость')

    plt.plot(rgb, label=['r', 'g', 'b'])
    plt.plot(luma, 'w', label='I')
    plt.legend()

    plt.imshow(background, origin='lower')

    plt.savefig(plot_name)


def read_intensity_by_length(photo_name, lamp, surface):
    coordinates = get_coordinates_mercury()

    rgb, luma = get_intensity_map(photo_name)

    k = (576.96 - 435.83) / (coordinates[576.96] - coordinates[435.83])
    first_pixel = 435.83 - k * coordinates[435.83]
    x = np.linspace(first_pixel, first_pixel + (X_RIGHT - X_LEFT) * k, X_RIGHT - X_LEFT)

    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))

    fig, ax = plt.subplots()
    plt.xlim(xmin=x.min(), xmax=x.max())

    plt.title('Интенсивность отражённого излучения\n' + '{} / {} поверхность'.format(lamp, surface))
    plt.xlabel('Длина волны, нм')
    plt.ylabel('Яркость')

    ax.set_facecolor('black')
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(5))
    plt.grid(color="grey")
    plt.ylim(ymin=0, ymax=max(luma.max(), rgb[::].max()) + 5)
    plt.plot(x, rgb, label=['r', 'g', 'b'])
    plt.plot(x, luma, 'w', label='I')
    plt.legend()


def read_intensity_by_length_multiple(photo_names, lamps, surfaces):
    fig, ax = plt.subplots()
    plt.title("Отражённая интенсивность излучения лампы накаливания")
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Яркость")
    ax.set_facecolor('grey')
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    plt.grid(color=(0.3, 0.3, 0.3))
    plt.grid(which="minor", color=(0.3, 0.3, 0.3), linestyle="--")

    coordinates = get_coordinates_mercury()

    k = (576.96 - 435.83) / (coordinates[576.96] - coordinates[435.83])
    first_pixel = 435.83 - k * coordinates[435.83]
    x = np.linspace(first_pixel, first_pixel + (X_RIGHT - X_LEFT) * k, X_RIGHT - X_LEFT)

    plt.xlim(xmin=x.min(), xmax=x.max())
    y_max = 0
    for photo_name, lamp, surface in zip(photo_names, lamps, surfaces):
        if lamp == "ртутная лампа":
            continue
        rgb, luma = get_intensity_map(photo_name)
        y_max = max(y_max, luma.max())
        plt.plot(x, luma, label=surface, color=COLORS[surface])

    plt.ylim(ymin=0, ymax=y_max + 5)

    plt.legend()


def albedos(photo_names, lamps, surfaces):
    fig, ax = plt.subplots()
    plt.title("Зависимость альбедо поверхностей от длины волны ")
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Яркость")
    ax.set_facecolor('grey')
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))
    plt.grid(color=(0.3, 0.3, 0.3))
    plt.grid(which="minor", color=(0.3, 0.3, 0.3), linestyle="--")

    coordinates = get_coordinates_mercury()

    k = (576.96 - 435.83) / (coordinates[576.96] - coordinates[435.83])
    first_pixel = 435.83 - k * coordinates[435.83]
    x = np.linspace(first_pixel, first_pixel + (X_RIGHT - X_LEFT) * k, X_RIGHT - X_LEFT)

    plt.xlim(xmin=x.min(), xmax=x.max())
    plt.ylim(ymin=0, ymax=1.2)

    d = dict()
    for photo_name, lamp, surface in zip(photo_names, lamps, surfaces):
        if lamp == "ртутная лампа":
            continue
        rgb, luma = get_intensity_map(photo_name)
        d[surface] = luma

    @np.vectorize
    def albedo(a, b):
        if b == 0:
            return 0
        if a / b >= 1.2:
            return 1
        return a / b

    for key in d:
        plt.plot(x, albedo(d[key], d["белая"]), label=key, color=COLORS[key])
    plt.legend()


def get_coordinates_mercury():
    rgb, luma = get_intensity_map("Pictures/mercury_light.jpg")

    return {435.83: np.argmax(rgb[:, 2]),
            546.074: np.argmax(rgb[:, 1]),
            576.96: np.argmax(rgb[:, 0])}
