# coding:utf-8
from datetime import datetime
import pickle
import yaml

from antColony import AntColony
from controllers.lagavulin.controllers.profilingAssistant import profilingAssistant


class antProfiler(profilingAssistant):
    def is_same(self, left, right):
        return True

if __name__ == '__main__':
    which_dataset = "../data/map_kanto_coord.pkl"

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
        verbose=False
    )

    pr = antProfiler()
    pr.profiling(aco.run_optimizer)