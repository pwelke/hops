#!/usr/bin/env python2

import sys
import numpy as np
import svmlight_loader as io
import scipy.sparse as sp

if __name__ == '__main__':	
	if (len(sys.argv) > 4) | (len(sys.argv) < 3):
		sys.stderr.write('libsvmFeatureFilter.py: Wrong number of arguments. Must be 2 or 3.\n')
		sys.exit(1)
	else:
		if (len(sys.argv) == 3):
			svmFilename = sys.argv[1]
			filterFile = sys.stdin
			outFilename = sys.argv[2]
		else: # len(sys.argv) == 4
			svmFilename = sys.argv[1]
			filterFile = open(sys.argv[2], 'r')
			outFilename = sys.argv[3]

	X,y = io.load_svmlight_file(svmFilename)
	featureSubset = np.loadtxt(filterFile)
	filterFile.close()

	sanitycheck = np.unique(featureSubset)
	print sanitycheck

	X_col = sp.csc_matrix(X)
	if X.shape[1] != featureSubset.shape[0]:
		sys.stderr.write('libsvmFeatureFilter.py: Dimension mismatch of filter and features. Assuming that the feature list is a prefix of the filter list.\n')
		featureSubset.resize(X.shape[1])

	# filter columns
	X_sub = X[:,featureSubset == 1]
	# sort matrix (o/w column indices are somehow inverted)
	X_sub.sort_indices()

	io.dump_svmlight_file(sp.csr_matrix(X_sub), y, outFilename)