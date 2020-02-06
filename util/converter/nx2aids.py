#!/usr/bin/env python3

import sys

import GraphDataToGraphList as d2l

def getLabel(objectData):
    if 'label' in objectData:
        # if there is label data, then the label data is a numpy array with values
        # here, we just return the first value as string
        return str(int(objectData['label'][0]))
    else:
        return 'None'


def nxGraphToText(index, g, label, output):
    vertexLabels = [getLabel(g.nodes[v]) for v in g.nodes]
    edges = [' '.join([str(e[0]), str(e[1]), getLabel(g.edges[e])]) for e in g.edges]

    output.write(' '.join(['#', str(index), str(label), str(g.number_of_nodes()), str(g.number_of_edges())]))
    output.write('\n')
    output.write(' '.join(vertexLabels))
    output.write('\n')
    output.write(' '.join(edges))
    output.write('\n')


def convertGraphList2AIDSFormat(path, db, output=sys.stdout):
    '''
    Convert graph dataset in the Dortmund collection to the format used by Pascal Welkes graph mining tools.

    Currently, vertex and edge labels will be the first dimension of the label vector, cast as int, or 'None' if there
    are no label information present. See getLabel above.

    Graphs will be numbered from 0 to N-1 if there are N graphs in the dataset.

    :param path: path to the unzipped location of the collection (must be terminated with '/'
    :param db: name of the dataset in the collection
    :param output: file like object (must provide a .write() function that accepts a string argument)
    :return: nothing
    '''
    graphStuff = d2l.graph_data_to_graph_list(path, db)
    graphs = graphStuff[0]
    labels = graphStuff[1]
    indices = range(len(graphs))

    for i, g, l in zip(indices, graphs, labels):
        nxGraphToText(i, g, l, output)
    output.writelines('$\n')


if __name__ == '__main__':
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        sys.stderr.write('nx2aids.py: incorrect number of arguments.\n'
                         'Usage: ' + sys.argv[0] + ' path_to_db/ dataset_name [output_file]\n'
                         '(was: ' + ' '.join(sys.argv) + ')\n')
    if len(sys.argv) == 4:
        out = open(sys.argv[3], 'w')
        convertGraphList2AIDSFormat(sys.argv[1], sys.argv[2], out)
        out.close()
    if len(sys.argv) == 3:
        convertGraphList2AIDSFormat(sys.argv[1], sys.argv[2])

