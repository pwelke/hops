import networkx as nx
import snap
import random
import math
from os import walk
import os
from graph_loader import snap_load
import time
from snap_hops import hops_estimation_recursive_snap
import pandas as pd
import matplotlib.pyplot as plt


def runtime_experiment(graphs_path, graph_names, patterns_path, output_path="experiments/", estimation_runtime=60,
                       repetitions=1, max_pattern_number=0, pattern_sizes=[10, 20, 30, 40, 50]):
    """
    Hops runtime experiments for large graphs in the .graph format of snap with different patterns
    :param graphs_path: path of the large graphs
    :param graph_names: names of the graphs in the .graph format
    :param patterns_path: path to the patterns of different sizes
    :param output_path: path to the output file of the experiments
    :param estimation_runtime: runtime of the Hops algorithm for one iteration
    :param repetitions: number of repetitions of the estimation of Hops for one pattern
    :param max_pattern_number: maximum number of considered patterns, if zero then all patterns are considered
    :param pattern_sizes: different sizes of the considered patterns
    """

    for size in pattern_sizes:  # go through all pattern sizes
        for graph_name in graph_names:  # go through all graphs
            results = {}
            counter = 0
            patterns = []
            # load the graph
            graph = snap_load(filename=graph_name,
                              src_path=graphs_path,
                              directed=True)
            for path in os.listdir(patterns_path + str(size) + "/"):  # go through all patterns of some size
                if max_pattern_number == 0 or counter < max_pattern_number:
                    results[path] = {}
                    abs_path = patterns_path + str(size) + "/" + path
                    pattern = snap_load(src_path=abs_path)
                    patterns.append(pattern)
                    results[path]["estimation"] = []
                    results[path]["number"] = []
                    results[path]["not_null"] = []
                    for j in range(repetitions):  # repeat the estimation for one graph and one pattern
                        start = time.time()
                        # run the Hops estimation
                        print("Start Estimation, Graph: {}, Pattern: {}".format(graph_name, path))
                        estimation_number, estimation = hops_estimation_recursive_snap(graph, pattern,
                                                                                       runtime=estimation_runtime,
                                                                                       labeled=False,
                                                                                       detailed_estimation=True)
                        print(time.time() - start)
                        estimation_count = len(estimation)
                        not_null_count = len([x for x in estimation if x != 0])
                        results[path]["estimation"].append(estimation_number)
                        results[path]["number"].append(estimation_count)
                        results[path]["not_null"].append(not_null_count)
                        print("Experiment: {} Estimation: {} Runs: {} Not null runs {}".format(j, estimation_number,
                                                                                               estimation_count,
                                                                                               not_null_count))
                    counter += 1

            # save the results
            df = pd.DataFrame(results)
            df.to_csv(output_path + "experiment_" + graph_name + "_runtime_" + str(estimation_runtime) + "_size_" + str(
                size) + ".csv")


def runtime_evaluation(graph_path, graphs, src_path="experiments/",
                       estimation_runtime=1, pattern_sizes=[10], normalized=False):
    graph_colors = [[128/255.0, 205/255.0, 193/255.0], [223/255.0, 194/255.0, 125/255.0], [166/255.0, 97/255.0, 26/255.0]]
    x_values = []
    y_values = []
    colors = []
    for i, graph in enumerate(graphs, 0):
        if normalized:
            G_snap = snap_load(graph, graph_path, directed=True)
            avg_node_degree = G_snap.GetEdges() * 2 / G_snap.GetNodes()
        for size in pattern_sizes:
            x = pd.read_csv(src_path + "experiment_" + graph + "_runtime_" + str(estimation_runtime) + "_size_" + str(
                size) + ".csv")
            x = x.to_dict()
            for x, y in x.items():
                estimation_list = y[0].strip('][').split(', ')
                iteration_list = y[1].strip('][').split(', ')
                not_null_iteration = y[2].strip('][').split(', ')

                if estimation_list[0] != 'estimation' and iteration_list[0] != 'number' and not_null_iteration[
                    0] != 'not_null':
                    x_values.append(size)
                    if normalized:
                        y_values.append((1.0 / (float(iteration_list[0]) * avg_node_degree)))
                    else:
                        y_values.append((1.0 / (float(iteration_list[0]))))
                    colors.append(graph_colors[i])
    plt.scatter(x_values, y_values, c=colors, alpha=0.5)
    plt.show()
