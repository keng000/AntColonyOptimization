

import matplotlib.pyplot as plt
import numpy as np
import pickle
from PIL import Image


def define_city(img_path, save_path):
    global_coor = []

    def onclick(event):
        # global global_coor
        global_coor.append([event.xdata, event.ydata])


    def set_town_point(img_path, save_path):
        img = np.asarray(Image.open(img_path))
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(15, 12, forward=True)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.imshow(img)
        plt.show()

        dic = {}
        for idx, data in enumerate(global_coor):
            dic[idx] = data

        with open(save_path, "wb") as f:
            pickle.dump(dic, f)

    set_town_point(img_path=img_path, save_path=save_path)


if __name__ == '__main__':

    define_city(
        img_path="../data/google_map_kanto.png",
        save_path="../data/map_kanto_coord.pkl"
    )
