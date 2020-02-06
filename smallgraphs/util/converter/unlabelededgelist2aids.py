#!/usr/bin/env python2

import sys
import numpy as np

'''Converter for labeled graphs.
Expects one input file:

* An edge list file of the format
vertex_x1 vertex_y1
vertex_x2 vertex_y2
...

All entries in the file are expected to be integers.
Vertex numbering is expected to start with 1.

2016-11-11 pwelke'''



# return unique rows of array
def unique(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1) 
    return a[ui]


# input format: vertex_1 vertex_2 label_id
# output: a list of undirected edges in the same format
# with vertex_1 < vertex_2 
# such an edge exists in the output iff at least one of the edges
# vertex_1 -> vertex_2 or vertex_2 -> vertex_1 exists in the input
#
# note that if an edge occurs more than once with different labels,
# tow edges are in the output, one for each label.
def undirected_edges(edges):
	reverse = np.hstack([edges[:,1].reshape([edges.shape[0],1]), edges[:,0].reshape([edges.shape[0],1]), edges[:,2].reshape([edges.shape[0],1])])
	# print reverse
	alledges = np.vstack([edges, reverse])
	idx = np.argsort(alledges[:,0])
	sortededges = alledges[idx,:]
	sortededges = sortededges[sortededges[:,0] < sortededges[:,1],:]
	return unique(sortededges)


# take output of undirected edges and a list of vertex labels and 
# print a graph in aids format to outfile.
def make_aids_format(vertex_labels, undirected_edges, outfile):
	outfile.write('# 0 0 ' + str(vertex_labels.shape[0]) + ' ' + str(undirected_edges.shape[0]) + '\n')
	for v in range(vertex_labels.shape[0]):
		outfile.write(str(int(vertex_labels[v])) + ' ')
	outfile.write('\n')
	for e in range(undirected_edges.shape[0]):
		for i in [0,1,2]:
			outfile.write(str(int(undirected_edges[e,i])) + ' ')
	outfile.write('\n$\n')

# run the conversion if this script runs on its own.
if __name__ == '__main__':
	unlabeledEdges = np.loadtxt(sys.argv[1])
	maxVertexId = np.max(unlabeledEdges)
	labeledEdges = np.hstack([unlabeledEdges, np.ones([unlabeledEdges.shape[0], 1])])

	vertexlabels = np.ones([maxVertexId, 1])
	edges = undirected_edges(labeledEdges)

	make_aids_format(vertexlabels, edges, sys.stdout)



