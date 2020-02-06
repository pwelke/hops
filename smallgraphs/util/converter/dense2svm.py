#!/usr/bin/env python2

import sys
import numpy as np
import svmlight_loader as io

'''
dense2svm.py Convert a dense array to an svm file in libsvm/svmlight format. 
Zero values in this array will be omitted from the output, as usual in sparse data format.
Command line input: labelfile datafile resultfile
labelfile: a one dimensional vector of labels, preferably -1 and 1 (not checked)
datafile: an array of values
labelfile and datafile have to be understandable by numpy.loadtxt

Stuff this program does for convenience and safety:
- checks if the dimensions of labels and data are matching [o/w error]

'''

def make_svm_file(labelfile, datafile, resultfile):
	y = np.loadtxt(labelfile)
	X = np.loadtxt(datafile)

	if len(y) != len(X):
		sys.stderr.write('dense2svm.py: Data and Labels have different dimensions. I give up.\n')
		return		

	io.dump_svmlight_file(X, y, resultfile)
	return

if __name__ == '__main__':
	if len(sys.argv != 4):
		sys.stderr.write('dense2svm.py: I take exactly three arguments: labelfile datafile resultfile')
	labelfile = sys.argv[1]
	datafile = sys.argv[2]
	resultfile = sys.argv[3]
	make_svm_file(labelfile, datafile, resultfile)
