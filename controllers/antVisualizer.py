# coding:utf-8
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pickle
from PIL import Image
import yaml

from antColony import AntColony


class antVisualizer(AntColony):
    def __init__(
            self, nodes, ant_num_of_each_nodes, init_pheromone_value, alpha, beta, rho, random, contrary,
            pheromone_constant, iterations, base_img_path,verbose=False
    ):

        super(antVisualizer, self).__init__(
            nodes, ant_num_of_each_nodes, init_pheromone_value, alpha, beta, rho,
            random, contrary, pheromone_constant, iterations, verbose
        )

        # for visualization
        self.base_img_path = base_img_path
        self.ax = None
        self.shortest_line_obj = []
        self.line_obj_box = [[0] * len(self.nodes) for _ in range(len(self.nodes))]
        self._visualize_graph(init=True)

    def run_optimizer(self):
        for _ in range(self.iterations):
            ants = self._init_ants()

            for ant in ants:
                ant.start_search()

            for ant in ants:
                if self.shortest_distance > ant.passed_distance:
                    self.shortest_distance = ant.passed_distance
                    self.shortest_path = ant.passed_route
                    # remove the previous lines
                    while self.shortest_line_obj:
                        one_line = self.shortest_line_obj.pop()
                        one_line.remove()

                    # plot lines when the shortest path is updated
                    for start in range(len(self.shortest_path) - 1):
                        obj, = self.ax.plot((self.nodes[self.shortest_path[start]][0],
                                             self.nodes[self.shortest_path[start + 1]][0]),
                                            (self.nodes[self.shortest_path[start]][1],
                                             self.nodes[self.shortest_path[start + 1]][1]),
                                            color="b", alpha=1.0, lw=1.5)

                        self.shortest_line_obj.append(obj)
                    plt.draw()
                self._map_one_ant_pheromone(ant)

            self._update_pheromone_mat()
            self._visualize_graph()

            if self.verbose and _ % 1 == 0:
                print("===result=== %d iterations" % _)
                print("shortest path is", self.shortest_path)
                print("shortest distance is ", self.shortest_distance)
                print("============\n")

    def _visualize_graph(self, init=False):
        if init is True:
            fig, self.ax = plt.subplots()
            # fig.set_size_inches(15, 12, forward=True)
            fig.set_size_inches(8, 6, forward=True)
            img = np.asarray(Image.open("../data/google_map_kanto.png"))
            plt.imshow(img)

            plt.xlim(0, img.shape[1])
            plt.ylim(img.shape[0], 0)

            # set each nodes as a scatter plot on the map
            for index in self.nodes.keys():
                x, y = self.nodes[index]
                self.ax.scatter(x, y)
                self.ax.annotate(index, (x + 1, y - 1), color="b")

            # plot pheromone density, and prepare objects of each lines.
            for start in range(len(self.pheromone_mat)):
                for end in range(len(self.pheromone_mat)):
                    self.line_obj_box[start][end], = self.ax.plot((self.nodes[start][0], self.nodes[end][0]),
                                                                  (self.nodes[start][1], self.nodes[end][1]), color="r")

        for start in range(len(self.pheromone_mat)):
            for end in range(len(self.pheromone_mat)):
                update_alpha = float(self.pheromone_mat[start][end]) / self.max_pheromone
                self.line_obj_box[start][end].set_alpha(update_alpha)

        plt.draw()
        plt.pause(0.01)


def run_visualizer(which_dataset, base_img_path):
    config = yaml.load(open("../config/aco_config.yml", "r"))
    nodes = pickle.load(open(which_dataset, "rb"))
    start_time = datetime.now()
    aco = antVisualizer(
        nodes=nodes,
        ant_num_of_each_nodes=config["ant_num_of_each_nodes"],
        init_pheromone_value=config["init_pheromone_value"],
        alpha=config["alpha"],
        beta=config["beta"],
        rho=config["rho"],
        random=config["random"],
        contrary=config["contrary"],
        pheromone_constant=config["pheromone_constant"],
        iterations=config["iterations"],
        base_img_path=base_img_path,
        verbose=True
    )

    aco.run_optimizer()

    print("===Final Result===")
    print("shortest path is", aco.shortest_path)
    print("shortest distance is ", aco.shortest_distance)
    print("============\n")
    print("Calculation time: %.3f seconds" % (datetime.now() - start_time).total_seconds())


if __name__ == '__main__':

    run_visualizer(
        which_dataset="../data/map_kanto_coord.pkl",
        base_img_path="../data/google_map_kanto.png"
    )
