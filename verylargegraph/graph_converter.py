import snap
import networkx as nx
import os


def txt_to_graph(filename, src_path, dst_path=""):
    """
    Converts a snap txt graph to the much more faster .graph format
    :param filename: name of the graph without .txt ending
    :param src_path: source path of the graph
    :param dst_path: destination path for the output
    """
    if dst_path == "":
        dst_path = src_path
    GSnap = snap.LoadEdgeList(snap.PNGraph, src_path + filename + ".txt")
    FOut = snap.TFOut(dst_path + filename + ".graph")
    GSnap.Save(FOut)


def graph_to_gpickle(filename, src_path, dst_path=""):
    if dst_path == "":
        dst_path = src_path
    G = nx.Graph()
    FIn = snap.TFIn(src_path + filename + ".graph")
    GSnap = snap.TNGraph.Load(FIn)
    edge_it = GSnap.BegEI()
    counter = 0
    while edge_it != GSnap.EndEI():
        G.add_edge(edge_it.GetSrcNId(), edge_it.GetDstNId())
        edge_it.Next()
        counter += 1
        print(counter)
    GSnap.Clr()
    nx.write_gpickle(G, dst_path)


def gml_gpickle_to_snap_graph(filename, src_path, dst_path=""):
    if dst_path == "":
        dst_path = src_path

    try:
        G = nx.read_gpickle(src_path + filename + ".gpickle")
    except:
        G = nx.read_gml(src_path + filename + ".gml")

    GSnap = snap.TUNGraph()

    labels = snap.TIntStrH()
    for node in G.nodes(data=True):
        id = node[0]
        node_label = node[1]['predicate']
        labels[int(id)] = str(node_label)
        GSnap.AddNode(int(id))

    for edge in G.edges():
        GSnap.AddEdge(int(edge[0]), int(edge[1]))

    FOut = snap.TFOut(dst_path + filename + ".graph")
    GSnap.Save(FOut)

    FOut = snap.TFOut(dst_path + filename + ".labels")
    labels.Save(FOut)
    FOut.Flush()


if __name__ == '__main__':
    txt_to_graph("com-youtube.ungraph", "D:/EigeneDokumente/PythonProjects/HOPS/snap_big_graphs/")
    print("Finished")
