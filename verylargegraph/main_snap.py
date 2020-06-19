from snap_experiments import runtime_experiment, runtime_evaluation
from graph_converter import txt_to_graph


def main():
    """
    Hops runtime evaluation with very large graphs
    """
    graphs_path = "D:/EigeneDokumente/PythonProjects/HOPS/snap_big_graphs/"
    patterns_path = "D:/EigeneDokumente/PythonProjects/HOPS/snap_random_trees/"
    graph_names = ["com-amazon.ungraph", "com-orkut.ungraph", "com-lj.ungraph"]
    pattern_sizes = [10, 20, 30, 40, 50]
    estimation_runtime = 60

    print("Start graph formatting")
    for graph in graph_names:
        txt_to_graph(graph, graphs_path)
    print("Formatted graphs to .graph")
    # uncomment for new run
    #print("Make runtime experiment")
    # runtime_experiment(graphs_path=graphs_path, graph_names=graph_names, patterns_path=patterns_path)
    print("Plot results")
    runtime_evaluation(graphs_path, graph_names, normalized=False,
                       estimation_runtime=estimation_runtime, pattern_sizes=pattern_sizes)
    runtime_evaluation(graphs_path, graph_names, normalized=True,
                       estimation_runtime=estimation_runtime, pattern_sizes=pattern_sizes)


if __name__ == '__main__':
    main()
