import itertools

import networkx as nx

from graph import graph_analyzer as ga


def find_all_groundings_of_predicates(data_graph,predicate1,predicate2):
    D=data_graph.copy()
    all_values1=ga.get_all_possible_nodes_wtih_values_in_data_graph(D,predicate1,False)
    all_nodes_constants=ga.get_all_possible_constants(D,predicate2)
    for c in all_nodes_constants:
        if not 'value' in c.keys():
           c['value']=c['name']
        c['target'] = 1
    for t in all_values1:
        t['target']=1
    output_graphs=[]
    for i in itertools.product(all_nodes_constants,all_values1):
        G = nx.Graph()
        G.add_node(1,i[0],valueinpattern=1,id=1)
        G.add_node(2,i[1],valueinpattern=1,id=2)
        G.add_edge(1,2)
        output_graphs.append(G)
    return output_graphs

def get_target_graph(predicate1,predicate2):
        G = nx.Graph()
        G.add_node(1,predicate=predicate1,label=predicate1,name=predicate1,valueinpattern=0,target=1,id=1)
        G.add_node(2,predicate=predicate2,label=predicate2,name=predicate2,valueinpattern=0,target=1,id=2)
        G.add_edge(1,2)
        return G



def ground_pattern(target_node,pattern):
    H = pattern.copy()
    for t in target_node:
       for n in H.nodes():
            if 'binds' in H.node[n].keys():
                if H.node[n]['predicate']==target_node.node[t]['predicate']:
                    H.node[n]['valueinpattern']=1
                    if 'value' in target_node.node[t].keys():
                        H.node[n]['value']=target_node.node[t]['value']
                    elif 'name' in target_node.node[t].keys():
                        H.node[n]['value'] = target_node.node[t]['name']
    return H


if __name__ == '__main__':
    data_graph = '/home/irma/work/DATA/DATA/yeast/YEAST.gpickle'
    data_graph = nx.read_gpickle(data_graph)
    tg=find_all_groundings_of_predicates(data_graph, 'function','constant')[0]
    pattern=nx.read_gml('/home/irma/work/DATA/DATA/yeast/pattern4.gml')
    ground_pattern=ground_pattern(tg,pattern)

