import subprocess
import os
# import numpy as np
import multiprocessing
from joblib import Parallel, delayed


def chunk_list(lst, n):
    """chunk list"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Experiment:
    """
    Base class of the experiments for hoPS
    """

    def __init__(self, main_path, main_out_path, data="yeast", pattern_sizes=[15], parallel_jobs=4,
                 time_step_exhaustive=3600, time_step_algos=2, time_limit_algos=60, time_limit_exhaustive=36000,
                 approaches=["exhaustive", "fk_AD", "fk_OBD", "fk_TREE", "random"]):
        self.main_path = main_path
        self.main_out_path = main_out_path
        self.data = data
        self.pattern_sizes = pattern_sizes
        self.parallel_jobs = parallel_jobs
        self.time_step_exhaustive = time_step_exhaustive
        self.time_step_algos = time_step_algos
        self.time_limit_algos = time_limit_algos
        self.time_limit_exhaustive = time_limit_exhaustive
        self.approaches = approaches

        # path of the approaches
        self.approaches_path = self.main_path + '/gs_srl/approaches/'
        # path of the graph data
        self.graph_data_path = self.main_path + '/data_ravkic/graphs/'
        # path of the tree patterns
        self.tree_patterns_data = self.main_path + '/data_ravkic/tree_patterns/'
        # path of the import files
        self.import_path = 'export PYTHONPATH="' + self.main_path + '/gs_srl/"'
        # path of the experiments output files
        # output_path = main_path + '/code/HOPS_Experiments/'
        self.output_path = self.main_path + self.main_out_path

        # name of the data folder together with the graph file
        self.graph_data = {"yeast": ("YEAST", "YEAST.gpickle"), "dblp": ("DBLP", "DBLP_2001-2_discretized.gpickle"),
                           "imdb": ("IMDB", "imdb.gml"), "webkb": ("WEBKB", "webkb.gml"),
                           "facebook": ("FACEBOOK", "facebook.gpickle"), "enron": ("ENRON", "enron.gpickle"),
                           "amazon": ("AMAZON", "amazon.gpickle")}
        self.data, self.pickle = self.graph_data[self.data]

        self.pattern_number = 0
        self.pattern_list = []

    def get_pattern_list(self):
        """
        Get all the tree patterns with certain conditions (size, ...)
        """
        patterns = []
        for subdir, dirs, files in os.walk(self.tree_patterns_data + self.data + '/'):
            for pattern in files:
                pattern_dict = {}
                pattern_size = subdir.split("_")[-1]  # get pattern size
                group = subdir.split("_")[-3]
                pattern_name = pattern.split(".")[0]
                pattern_path = subdir + "/" + pattern
                pattern_dict = {"name": pattern_name, "size": pattern_size, "path": pattern_path}

                if int(pattern_size) in self.pattern_sizes:
                    patterns.append(pattern_dict)

        self.pattern_number = len(patterns)
        pattern_list = list(
            chunk_list(sorted(patterns, key=lambda i: i['name']), max(1, (self.pattern_number + self.parallel_jobs) // self.parallel_jobs)))
        print(len(pattern_list), pattern_list)
        self.pattern_list = pattern_list
        return pattern_list

    def run_one_exp(self, j):
        """
        Run the experiment for all approaches over a sublist of the pattern list
        """
        num = len(self.pattern_list[j])
        for i, pattern in enumerate(self.pattern_list[j], 0):
            pattern_size = str(pattern["size"])  # get pattern size
            pattern_name = pattern["name"]
            pattern_path = pattern["path"]

            print("Consider Pattern: " + pattern_name + " of size " + pattern_size)
            if "exhaustive" in self.approaches:
                print("Max Time remaining: " + str(
                    (num - i) * (int(self.time_limit_exhaustive) + 10) / 3600 + (len(self.approaches) - 1) * (
                                num - i) * (int(self.time_limit_algos) + 10) / 3600) + " h")
            else:
                print("Max Time remaining: " + str(
                    len(self.approaches) * (num - i) * (int(self.time_limit_algos) + 10) / 3600) + " h")

            print(str(i + 1) + "/" + str(num))

            for approach in self.approaches:
                if approach == "exhaustive":
                    max_time = str(self.time_limit_exhaustive)
                    time_interval = str(self.time_step_exhaustive)
                else:
                    max_time = str(self.time_limit_algos)
                    time_interval = str(self.time_step_algos)

                print("Running: " + approach + "_approach")

                with open(self.output_path + approach + '_approach' + "_" + pattern_name, 'w') as rsh:
                    rsh.write(
                        '''#!/bin/sh\n''' + self.import_path + '''\n''' + '''python2 ''' + self.approaches_path + approach + '''_approach.py -d ''' + self.graph_data_path + self.data + '''/''' + self.pickle + ''' -p ''' + pattern_path + ''' -o ''' + self.output_path + '''Results/''' + self.data + '''/pattern_size''' + pattern_size + '''/''' + pattern_name + '''/ -t ''' + time_interval + ''' -max_time ''' + max_time)

                os.chmod(self.output_path + approach + "_approach" + "_" + pattern_name, 0o755)

                subprocess.call(self.output_path + approach + '_approach' + "_" + pattern_name)

                print("Finished: " + approach + "_approach")

    def run_experiment(self):
        """
        Run the embedding algorithms parallelized for all the patterns
        """
        self.get_pattern_list()
        Parallel(n_jobs=self.parallel_jobs)(delayed(self.run_one_exp)(i) for i in range(len(self.pattern_list)))


def main():
    """
    Run the experiments of the hoPS paper
    main_path: path of the graph and pattern data
    main_out_path: path of the experiments output data
    data: data to run the experiments from [yeast, dblp, imdb, webkb, facebook, amazon]
    pattern_sizes: list of sizes of the patterns to run the experiments
    parallel_jobs: number of kernels to run the experiments
    time_limit_exhaustive: time limit of exact algorithm in seconds
    time_step_exhaustive: time steps of monitoring output of exact algorithm in seconds
    time_limit_algos: time limit of algorithms in seconds
    time_step_algos: time steps of monitoring output of algorithms in seconds
    approaches: used algorithms from ["exhaustive", "fk_AD", "fk_OBD", "fk_TREE", "random"] (note that at first exhaustive has to be executed, due to implementation of Ravkic et al.)
    """

    main_path = "/home/.../largegraph" #TODO set your path
    #Settings used for paper experiments
    for val in [("YEAST", "yeast", [15]), ("WEBKB", "webkb", [10]), ("DBLP", "dblp", [10]), ("FACEBOOK", "facebook", [6])]:
        for a in val[2]:
            program = Experiment(main_path=main_path,
                                 main_out_path='/HopsExperiments/Experiments' + val[0] + '10h/', data=val[1],
                                 pattern_sizes=[a], parallel_jobs=4, time_limit_exhaustive=36000,
                                 time_step_exhaustive=3600, time_limit_algos=60, time_step_algos=2,
                                 approaches=["exhaustive", "fk_AD", "fk_OBD", "fk_TREE", "random"])
            program.run_experiment()
    
    

if __name__ == "__main__":
    main()
