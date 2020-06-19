import random
import numpy as np
import networkx as nx
import scipy
from multiprocessing import Pool
import snap
from time import sleep
import time
from threading import Thread
from joblib import Parallel, delayed


def n_max_matchings(A, B):
    """
    Compute the number of maximum matchings in a complete bipartite graph on A + B vertices.
    A and B are required to be nonnegative.
    Corner Case: If at least one of the sides has zero vertices, there is one maximal matching: the empty set.
    """
    a = min(A, B)
    b = max(A, B)
    c = 1

    if a != 0:
        for i in range(b - a + 1, b + 1):
            c *= i

    return c


def uniformRandomMaximumMatching_snap(N_u, N_v, H_labels, G_labels, labeled):
    """
    Draw a maximum matching from a block disjoint bipartite graph uniformly at random and return it and
    the number of such matchings.

    Which vertex x can be assigned to which vertex y is given by x['predicate'] == y['predicate']

    :param N_u: list of vertices from H that must be assigned
    :param N_v: list of vertices from G that can be assigned to
    :return: M, c : a matching M, given as a map and the number of all maximum matchings c
    """

    hu = dict()
    hv = dict()
    c = 1

    # create blocks of identical symbols
    if labeled:
        for x in N_u:
            try:
                hu[H_labels[x]].append(x)
            except KeyError:
                hu[H_labels[x]] = [x]

        for y in N_v:
            try:
                hv[G_labels[y]].append(y)
            except KeyError:
                hv[G_labels[y]] = [y]
    else:
        for x in N_u:
            try:
                hu["label"].append(x)
            except KeyError:
                hu["label"] = [x]

        for y in N_v:
            try:
                hv["label"].append(y)
            except KeyError:
                hv["label"] = [y]

    # shuffle target list
    for y in hv.keys():
        random.shuffle(hv[y])

    # compute uniform random maximal matching
    matching = dict()
    for x in hu.keys():
        try:
            for i, j in zip(hu[x], hv[x]):
                matching[i] = j
            c *= n_max_matchings(len(hu[x]), len(hv[x]))
        except KeyError:
            pass
    return matching, c


def find_tree_embeddings_snap(u, v, phi, phi_inv, H, H_labels, G, G_labels, labeled):
    node_iterator = H.GetNI(u)
    neighbors_H_num = node_iterator.GetDeg()
    U_n = [node_iterator.GetNbrNId(i) for i in range(neighbors_H_num) if
           node_iterator.GetNbrNId(i) not in phi.keys()]

    node_iterator = G.GetNI(v)
    neighbors_G_num = node_iterator.GetDeg()
    V_n = [node_iterator.GetNbrNId(i) for i in range(neighbors_G_num) if
           node_iterator.GetNbrNId(i) not in phi_inv.keys()]

    M, c = uniformRandomMaximumMatching_snap(U_n, V_n, H_labels, G_labels, labeled)
    if len(M) == len(U_n):
        # add matching to phi
        for x in M.keys():
            y = M[x]
            phi[x] = y
            phi_inv[y] = x
        # recurse
        for x in M.keys():
            c_rec, phi, phi_inv = find_tree_embeddings_snap(x, M[x], phi, phi_inv, H, H_labels, G, G_labels, labeled)
            c *= c_rec
            if c == 0:
                break
    else:
        c = 0

    return c, phi, phi_inv


def label_frequency_histogram_snap(labels):
    '''
    Given  a data graph, find histogram w.r.t. predicate names of the nodes. The method returns
    a list of tuples sorted from least occurring to most occurring nodes in the graph.
    :param data_graph_path: path to the domain graph
    :param labels: labels of interest
    :return: return list of tuples (predicate_name,number_of_occurences) (sorted from least occurring, to most occurring)
    '''

    f = lambda x, d={}: ([d.__setitem__(x[key], d.get(x[key], 0) + 1) for key in x], d)[
        -1]
    hist = f(labels)
    return {k: v for k, v in sorted(hist.items(), key=lambda item: item[1])}


def get_pattern_root_node_snap(P_labels, hist):
    for k, v in hist.items():
        root_node_predicate_name = k  # choose the root node predicate
        possible_root_nodes = [key for key in P_labels if
                               P_labels[key] == root_node_predicate_name]
        if (len(possible_root_nodes) == 0):
            continue

        ran = random.randint(0, len(possible_root_nodes) - 1)
        root_node = possible_root_nodes[ran]
        return root_node, root_node_predicate_name


def hops_estimation_recursive_snap(G, H, G_labels=snap.TIntStrH(), H_labels=snap.TIntStrH(), k=0, runtime=0,
                                   labeled=True, detailed_estimation=False):
    """

    :param G: graph
    :param H: pattern graph
    :param G_labels: vector of graph labels
    :param H_labels: vector of pattern labels
    :param k: number of iterations of hops for one iteration
    :param runtime: runtime of hops for one estimation
    :param labeled: determines if graph and pattern are labeled
    :param detailed_estimation: if output should be detailed
    :return: in case of detailed estimation return estimation count and single iteration steps, else only return estimation count
    """
    estimation_values = []

    if labeled:
        pattern_root_node, root_node_predicate_name = get_pattern_root_node_snap(H_labels,
                                                                                 label_frequency_histogram_snap(
                                                                                     G_labels))

        possible_root_nodes = [x.GetId() for x in G.Nodes() if G_labels[x.GetId()] == root_node_predicate_name]
    else:
        pattern_root_node = H.GetRndNId()
        possible_root_nodes = [x.GetId() for x in G.Nodes()]

    if runtime != 0:
        t_end = time.time() + runtime
        while time.time() < t_end:
            v = possible_root_nodes[random.randint(0, len(possible_root_nodes) - 1)]

            c, phi, phi_inv = find_tree_embeddings_snap(pattern_root_node, v, {pattern_root_node: v},
                                                        {v: pattern_root_node},
                                                        H, H_labels,
                                                        G, G_labels, labeled)
            c *= len(possible_root_nodes)
            estimation_values.append(c)
    else:
        for i in range(0, k):
            # sample root node and sample first image of u
            v = possible_root_nodes[random.randint(0, len(possible_root_nodes) - 1)]

            c, phi, phi_inv = find_tree_embeddings_snap(pattern_root_node, v, {pattern_root_node: v},
                                                        {v: pattern_root_node},
                                                        H, H_labels,
                                                        G, G_labels, labeled)
            c *= len(possible_root_nodes)
            estimation_values.append(c)
    if len(estimation_values) == 0:
        return 0, [0]
    if detailed_estimation:
        return sum(estimation_values) / len(estimation_values), estimation_values
    else:
        return sum(estimation_values) / len(estimation_values)
