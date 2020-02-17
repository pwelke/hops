

from sampling_core import sampler_general_ex as ad
from approaches import prepare_inputs
from OBDs import OBDsearch

import argparse,os,time,random, math


def get_nr_embedding(data_graph, pattern, root_node, root_nodes, n_iter):

    sum_estimates = 0
    estimates = list()

    start = time.time()

    OBdecomp = OBDsearch.get_heuristic4_OBD(pattern, startNode=root_node)


    for iteration_counter in range(n_iter):

        # sample first image of u
        vi = random.randrange(len(root_nodes))
        v = root_nodes[vi]

        list_for_spent = []
        list_for_spent.append(1)

        result = ad.find_embeddings_Furer([v], data_graph, pattern, OBdecomp, 0, [], list_for_spent, None, None, None, None)

        c = result[0] * len(root_nodes)

        estimates.append(c)
        sum_estimates += c

    end = time.time()
    nr_emb = sum_estimates / float(n_iter)
    stddev = math.sqrt(sum([(x - nr_emb) ** 2 for x in estimates])) / float(n_iter)

    print('n_iter', n_iter)
    print('time', end - start)
    print('estimate', nr_emb)
    print('stddev', stddev)

    return nr_emb, estimates


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Running FK-OBD or FK-AD approach')
    parser.add_argument('-d', help='path to data file')
    parser.add_argument('-p', help='path to pattern file')
    parser.add_argument('-o', help='output path')
    parser.add_argument('-exh', help='path to ground truth results (if statistics needed)')
    parser.add_argument('-runs', default=20000, type=int, help='Number of iterations. Default=1000')
    parser.add_argument('-t', default=300, type=int, help='time interval in seconds')
    parser.add_argument('-write', default=True, action='store_false',help='save to disk pickles having all the embeddings')
    parser.add_argument('-root_node_id',default=None, type=int,help='id of a root node')
    parser.add_argument('-root_node_name', default=None, help='name of a root node')
    parser.add_argument('-max_time', default=36000, type=int, help='maximum sampling time')

    args = parser.parse_args()

    #Preparing the inputs
    data_graph, pattern, _, root_node, root_node_predicate_name, interval, max_time, monitoring_marks, root_nodes, _ = prepare_inputs.prepare_params(args)
    n_iter = args.runs
    # output_folder='fk_TREE_results'
    # output_path=os.path.join(args.o,output_folder)
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    get_nr_embedding(data_graph, pattern, root_node, root_nodes, n_iter)
