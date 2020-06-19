import networkx as nx
import snap
import random
import math


def create_rnd_trees(size, number, filename, dst_path, labeled=False, seed=1):
    random.seed(seed)
    for i in range(number):
        G = nx.random_tree(size, seed + i)
        GSnap = snap.TUNGraph()

        if labeled:
            labels = snap.TIntStrH()
        for node in G.nodes(data=True):
            id = node[0]
            if labeled:
                node_label = node[1]['predicate']
                labels[int(id)] = str(node_label)
            GSnap.AddNode(int(id))

        for edge in G.edges():
            GSnap.AddEdge(int(edge[0]), int(edge[1]))

        FOut = snap.TFOut(dst_path + filename + "_" + str(i).zfill(math.ceil(math.log10(number + 1))) + ".graph")
        GSnap.Save(FOut)
        FOut.Flush()

        if labeled:
            FOut = snap.TFOut(dst_path + filename + "_" + str(i).zfill(math.ceil(math.log10(number + 1))) + ".labels")
            labels.Save(FOut)
            FOut.Flush()


def main():
    size = 50
    number = 50
    create_rnd_trees(size, number, "rnd_tree", "D:\\EigeneDokumente\\PythonProjects\\HOPS\\random_trees_snap\\"+ str(size) + "\\")


if __name__ == '__main__':
    main()
