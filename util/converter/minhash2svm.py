#!/usr/bin/env python2

import sys
import numpy as np
import svmlight_loader as io

'''
minhash2svm.py Convert a minhash dense array to an svm file in libsvm/svmlight format. 
Command line input: labelfile datafile resultfile
labelfile: a one dimensional vector of labels, preferably -1 and 1 (not checked)
datafile: an array of nonnegative values
labelfile and datafile have to be understandable by numpy.loadtxt

Stuff this program does for convenience and safety:
- checks if the dimensions of labels and data are matching [o/w error]
- checks if data contains negative values [o/w error]
- checks if data contains zeros [then add one to every value, generate warning]

'''

def make_svm_file(labelfile, datafile, resultfile):
	y = np.loadtxt(labelfile)
	X = np.loadtxt(datafile)

	if len(y) != len(X):
		sys.stderr.write('minhash2svm.py: Data and Labels have different dimensions. I give up.\n')
		return		

	# Check if data is nonnegative.
	# Also check if data contains zeros. If so, shift values up and generate a warning
	unique_values = np.unique(X)
	zero_count = (unique_values == 0).sum()
	nonnegative_count = (unique_values >= 0).sum()
	if nonnegative_count == unique_values.shape[0]:
		if zero_count > 0:
			sys.stderr.write('minhash2svm.py: Data file contains zero positions. Shifting values up by one.\n')
			X = X + 1
	else:
		sys.stderr.write('minhash2svm.py: Data file contains nonpositive values. I give up.\n')
		return

	io.dump_svmlight_file(X, y, resultfile)
	return

if __name__ == '__main__':
	if len(sys.argv != 4):
		sys.stderr.write('minhash2svm.py: I take exactly three arguments: labelfile datafile resultfile')
	labelfile = sys.argv[1]
	datafile = sys.argv[2]
	resultfile = sys.argv[3]
	make_svm_file(labelfile, datafile, resultfile)
