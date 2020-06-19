import snap
import networkx as nx
import os
import graph_converter


def test_graphs():
    G_nodes = [0, 1, 2]
    G_edges = [(0, 1), (0, 2), (1, 2)]
    H_nodes = [x for x in range(6)]
    H_edges = [(0, 1), (0, 5), (2, 4), (0, 3), (1, 2)]
    G1 = snap.TNGraph.New()
    for x in G_nodes:
        G1.AddNode(x)
    for x, y in G_edges:
        G1.AddEdge(x, y)
    H1 = snap.TNGraph.New()
    for x in H_nodes:
        H1.AddNode(x)
    for x, y in H_edges:
        H1.AddEdge(x, y)

    G2 = nx.Graph()
    for x, y in G_edges:
        G2.add_edge(x, y)
    H2 = nx.Graph()
    for x, y in H_edges:
        H2.add_edge(x, y)
    return G1, H1, G2, H2


def snap_load(filename="", src_path="", directed=False):
    graph_extension = ".graph"
    label_extension = ".label"
    if filename == "":
        graph_extension = ""

    if os.path.isfile(src_path + filename + graph_extension):
        g_path = src_path + filename + graph_extension
        FIn = snap.TFIn(g_path)
        if directed:
            G = snap.TNGraph.Load(FIn)
        else:
            G = snap.TUNGraph.Load(FIn)
    elif os.path.isfile(src_path + filename + ".gml") or os.path.isfile(src_path + filename + ".gpickle"):
        graph_converter.gml_gpickle_to_snap_graph(filename, src_path)
        FIn = snap.TFIn(src_path + filename + graph_extension)
        if directed:
            G = snap.TNGraph.Load(FIn)
        else:
            G = snap.TUNGraph.Load(FIn)
    if os.path.isfile(src_path + filename + label_extension):
        FIn = snap.TFIn(src_path + filename + label_extension)
        labels = snap.TIntStrH()
        labels.Load(FIn)
    else:
        labels = snap.TIntStrH()

    if labels:
        return G, labels
    else:
        return G


def nx_load(filename, src_path):
    try:
        G = nx.read_gpickle(src_path + filename + ".gpickle")
    except:
        G = nx.read_gml(src_path + filename + ".gml")
    return G
