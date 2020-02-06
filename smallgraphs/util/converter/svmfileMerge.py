#!/usr/bin/env python2

import scipy.sparse as sp
import svmlight_loader as io
import sys

'''Merge two files in svmlight / libSVM sparse format.'''

def mergeSparse(f1, f2, f3): 
	X1, y1 = io.load_svmlight_file(f1)
	X2, y2 = io.load_svmlight_file(f2)

	if (y1.shape == y2.shape):
		X = sp.hstack([X1, X2])
	else:
		sys.stderr.write('Error: Different number of examples in files: ' + str(y1.shape) + ' != ' + str(y2.shape) + '\n')
		return

	if (y1 == y2).sum() != y1.shape[0]:
		sys.stderr.write('Warning: Label mismatch. Are you merging features of the same subset?\nI will use the labels of the first argument\n')

	y = y1
	io.dump_svmlight_file(X, y, f3)
	return

if __name__ == '__main__':
	if (len(sys.argv) != 4):
		sys.stderr.write('This script takes exactly three parameters. Infile1, Infile2, and Outfile. You specified ' + str(len(sys.argv)) + '\n')
	f1 = sys.argv[1]
	f2 = sys.argv[2]
	f3 = sys.argv[3]
	mergeSparse(f1, f2, f3)





