# coding:utf-8
from datetime import datetime
import math
import numpy as np
import pickle
import yaml


class AntColony(object):
    class Ant(object):
        def __init__(self, initial_position, distance_mat, pheromone_mat, alpha, beta, random, contrary, pheromone_constant):

            self.distance_mat = distance_mat
            self.pheromone_mat = pheromone_mat

            self.initial_vertex = initial_position
            self.recent_vertex = initial_position
            self.passed_route = [initial_position]

            self.alpha = alpha
            self.beta = beta
            self.random = random
            self.contrary = contrary
            self.pheromone_constant = pheromone_constant

            self.possible_vertices = list(range(len(distance_mat)))
            self.possible_vertices.remove(initial_position)

            self.passed_distance = 0

            self.tau_matrix = np.zeros(self.pheromone_mat.shape)

        def start_search(self):
            while self.possible_vertices:
                next_vertex = self._choose_next_vertex()
                self._move_to_next_vertex(recent=self.recent_vertex, next_=next_vertex)

            self.passed_distance += self.distance_mat[self.recent_vertex, self.initial_vertex]
            self.recent_vertex = self.initial_vertex
            self.passed_route.append(self.initial_vertex)
            self._map_pheromone()

        def _move_to_next_vertex(self, recent, next_):
            self.passed_distance += self.distance_mat[recent][next_]
            self.recent_vertex = next_
            self.passed_route.append(next_)
            self.possible_vertices.remove(next_)

        def _choose_next_vertex(self):
            method = np.random.choice([self._adaptive_to_pheromone, self._random_choice, self._contrary_to_pheromone],
                                      p=[(1.0 - self.random - self.contrary), self.random, self.contrary])

            return method()

        def _contrary_to_pheromone(self):
            each_path_weight = np.zeros(len(self.possible_vertices))

            for idx, possible_vertex in enumerate(self.possible_vertices):
                pheromone_amount = self.pheromone_mat[self.recent_vertex, possible_vertex]
                distance = self.distance_mat[self.recent_vertex, possible_vertex]
                possibility = np.power(1.0 / pheromone_amount, self.alpha) * np.power(1.0 / distance, self.beta)
                each_path_weight[idx] = possibility

            possibility_list = each_path_weight / np.sum(each_path_weight)
            return np.random.choice(self.possible_vertices, p=possibility_list)

        def _random_choice(self):
            return np.random.choice(self.possible_vertices)

        def _adaptive_to_pheromone(self):
            each_path_weight = np.zeros(len(self.possible_vertices))

            for idx, possible_vertex in enumerate(self.possible_vertices):
                pheromone_amount = self.pheromone_mat[self.recent_vertex, possible_vertex]
                distance = self.distance_mat[self.recent_vertex, possible_vertex]
                possibility = np.power(pheromone_amount, self.alpha) * np.power(1.0 / distance, self.beta)
                each_path_weight[idx] = possibility

            possibility_list = each_path_weight / np.sum(each_path_weight)
            return np.random.choice(self.possible_vertices, p=possibility_list)

        def _map_pheromone(self):
            for vertex_idx in range(len(self.passed_route) - 1):
                pheromone_delta = float(self.pheromone_constant) / self.passed_distance
                self.tau_matrix[self.passed_route[vertex_idx], self.passed_route[vertex_idx + 1]] += pheromone_delta

    def __init__(self, nodes, ant_num_of_each_nodes, init_pheromone_value, alpha, beta, rho, random, contrary,
                 pheromone_constant, iterations, verbose=False):

        self.nodes = nodes
        self.distance_mat = self._create_distance_mat(nodes=nodes)
        self.ant_num = len(self.nodes) * ant_num_of_each_nodes
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.rho = float(rho)
        self.random = float(random)
        self.contrary = float(contrary)
        self.pheromone_constant = float(pheromone_constant)
        self.iterations = iterations
        self.verbose = verbose

        # returns a ndarray
        self.pheromone_mat = self._init_mat(len(self.distance_mat), init_pheromone_value)
        self.tau_matrix = self._init_mat(len(self.distance_mat), 0)
        self.max_pheromone = 1.0
        self.min_pheromone = 0

        self.shortest_path = None
        self.shortest_distance = float("inf")

    def run_optimizer(self):
        for _ in range(self.iterations):
            ants = self._init_ants()

            for ant in ants:
                ant.start_search()

            for ant in ants:
                if self.shortest_distance > ant.passed_distance:
                    self.shortest_distance = ant.passed_distance
                    self.shortest_path = ant.passed_route

                self.tau_matrix += ant.tau_matrix

            self._update_pheromone_mat()

            if self.verbose and _ % 1 == 0:
                print("===result=== %d iterations" % _)
                print("shortest path is", self.shortest_path)
                print("shortest distance is ", self.shortest_distance)
                print("============\n")

    def _create_distance_mat(self, nodes):
        '''
        create a distance matrix from node dictionary
        '''
        distance_mat = self._init_mat(len(nodes), 0.0)
        for idx in range(len(nodes)):
            for jdx in range(len(nodes)):
                x_distance = abs(nodes[idx][0] - nodes[jdx][0])
                y_distance = abs(nodes[idx][1] - nodes[jdx][1])
                distance_mat[idx, jdx] = math.sqrt(x_distance * x_distance + y_distance * y_distance)

        return distance_mat

    def _init_mat(self, length, value):
        return np.ones((length, length), dtype=float) * value

    def _init_ants(self):
        '''
        In this version, ants are set to each node in order.
        So that to keep fairness between each nodes, the number of ants should be a multiple of the number of nodes.
        '''
        return [self.Ant(initial_position=idx % len(self.distance_mat), distance_mat=self.distance_mat,
                         pheromone_mat=self.pheromone_mat, alpha=self.alpha, beta=self.beta, random=self.random,
                         contrary=self.contrary, pheromone_constant=self.pheromone_constant) for idx in range(self.ant_num)]

    def _update_pheromone_mat(self):
        self.pheromone_mat = self.pheromone_mat * self.rho + self.tau_matrix
        self.pheromone_mat[self.pheromone_mat <= self.min_pheromone] = self.min_pheromone
        self.pheromone_mat[self.pheromone_mat >= self.max_pheromone] = self.max_pheromone
        self.tau_matrix = self._init_mat(len(self.distance_mat), 0)


def run_calculation(which_dataset):
    config = yaml.load(open("../config/aco_config.yml", "r"))

    nodes = pickle.load(open(which_dataset, "rb"))
    start_time = datetime.now()
    aco = AntColony(
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
        verbose=True
    )

    aco.run_optimizer()

    print("===Final Result===")
    print("shortest path is", aco.shortest_path)
    print("shortest distance is ", aco.shortest_distance)
    print("============\n")
    print("Calculation time: %.3f seconds" % (datetime.now() - start_time).total_seconds())


if __name__ == '__main__':

    run_calculation(which_dataset="../data/map_kanto_coord.pkl")
