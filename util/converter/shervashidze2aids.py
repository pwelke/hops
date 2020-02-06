#!/usr/bin/env python2

import sys
import numpy as np
from scipy.io import loadmat

'''This is a converter specifically designed to eat the format
of the matlab graph databases provided by Nino Shervashidze at
http://www.di.ens.fr/~shervashidze/code.html.

Works for all datasets, except for the two NCI*. There, positions
of vertex labels and incidence matrix are exchanged. I love it.
Use ShervashidzeNCI2aids.py insteadd'''

def transform(filename, dataname, labelname, out, err):

	data = loadmat(filename)
	err.write('keys of the loaded struct are:\n')
	err.write(' '.join(data.keys()) + '\n')
	graphs = data[dataname]
	labels = data[labelname]

	for i in range(graphs.shape[1]):
		graphLabel = labels[i][0]
		vertexLabels = graphs[0,i][1]
		try:
			m = graphs[0,i][0].nnz / 2
			edges = graphs[0,i][0].todense()
		except:
			edges = graphs[0,i][0]
			m = (edges > 0.0).sum() / 2

		n = vertexLabels[0][0][0].shape[0]
		out.write(' '.join(['#', str(i+1), str(graphLabel), str(n), str(m)]))
		out.write('\n')
		out.write(' '.join([str(vertexLabels[0][0][0][v][0]) for v in range(n)]))
		out.write('\n')
		for v in range(n):
			for w in range(v, n):
				if (edges[v,w] > 0):
					out.write(str(v+1) + ' ' + str(w+1) + ' ' + str(int(edges[v,w])) + ' ')
		out.write('\n')

	out.write('$\n')

if __name__ == '__main__':
	filename = sys.argv[1]
	dataname = sys.argv[2]
	labelname = sys.argv[3]
	transform(filename, dataname, labelname, sys.stdout, sys.stderr)