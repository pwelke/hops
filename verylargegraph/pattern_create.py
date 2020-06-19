import networkx as nx
import snap
import random
import math


def create_rnd_trees(size, number, dst_path, seed=1):
    """
    Creates some number of random trees of some size
    :param size: size of the random trees
    :param number: number of random trees to generate
    :param dst_path: output path for the patterns
    :param seed: seed for the randomness
    """
    random.seed(seed)
    for i in range(number):
        G = nx.random_tree(size, seed + i)
        GSnap = snap.TUNGraph()
        for edge in G.edges():
            GSnap.AddEdge(int(edge[0]), int(edge[1]))

        FOut = snap.TFOut(dst_path + "rnd_tree" + "_" + str(i).zfill(math.ceil(math.log10(number + 1))) + ".graph")
        GSnap.Save(FOut)
        FOut.Flush()


def main():
    size = 50
    number = 50
    create_rnd_trees(size, number, "rnd_tree",
                     "D:\\EigeneDokumente\\PythonProjects\\HOPS\\random_trees_snap\\" + str(size) + "\\")
