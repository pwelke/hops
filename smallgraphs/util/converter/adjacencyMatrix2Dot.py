def adjacencyMatrix2dot(am, out):
	'''Take a numpy adjacency matrix and write the corresponding graph in the dot language to
	out. out must be a writeable file, such as f = open('some/path/', 'w'), or sys.stdout'''

	# print graph header
	out.write('digraph {\n')

	# write vertices
	n = am.shape[0]
	for i in range(n):
		out.write('{0} [label={0}];\n'.format(str(i)))

	# write edges with labels
	edges = np.nonzero(am)
	edgeLabels = am[edges]
	edgeIds = np.transpose(edges)
	for i in range(edgeIds.shape[0]):
		out.write('{0} -> {1} [label={2}];\n'.format(str(edgeIds[i,0]), str(edgeIds[i,1]), str(edgeLabels[i])))

	# terminate graph description
	out.write('}\n')

def adjacencyMatrixDiff2dot(old, new, out):
	'''Take two numpy adjacency matrices and write the corresponding graph with highlighted differences
	in the dot language to out. 
	Edges that appear in both old and new are black, 
	edges that are only in old are red, 
	edges that are only in new are green.

	out must be a writeable file, such as f = open('some/path/', 'w'), or sys.stdout
	'''

	# check whether matrix dimensions match and matrices are quadratic
	if (old.shape[0] != old.shape[1]) 
		|| (old.shape[0] != new.shape[0]) 
		|| (old.shape[1] != new.shape[1]) 
		|| (len(old.shape) != len(new.shape)):

		raise Error('Matrix dimensions mismatch: {} != {}'.format(str(old.shape), str(new.shape)))

	# print graph header
	out.write('digraph {\n')

	# write vertices
	n = old.shape[0]
	for i in range(n):
		out.write('{0} [label={0}];\n'.format(str(i)))

	# write edges with labels
	o_edges = np.nonzero(old)
	o_edgeLabels = old[o_edges]
	o_edgeIds = np.transpose(o_edges)

	blackEdges = np.nonzero

	for i in range(edgeIds.shape[0]):
		out.write('{0} -> {1} [label={2}];\n'.format(str(edgeIds[i,0]), str(edgeIds[i,1]), str(edgeLabels[i])))

	# terminate graph description
	out.write('}\n')