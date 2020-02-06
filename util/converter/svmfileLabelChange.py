#!/usr/bin/env python2

import scipy.sparse as sp
import svmlight_loader as io
import numpy as np
import sys

def AvsI(x):
	if x == 0:
		return -1
	if x == 2:
		return 1
	return 0

def AMvsI(x):
	if x == 0:
		return -1
	if x == 1:
		return 1
	if x == 2:
		return 1
	return 0

def AvsMI(x):
	if x == 0:
		return -1
	if x == 1:
		return -1
	if x == 2:
		return 1
	return 0


def changeSparseLabels(f1, f2, labelFunction=AvsI): 
	Xold, yold = io.load_svmlight_file(f1)

	vectorizedFunction = np.vectorize(labelFunction, otypes=[np.int32])
	ynew = vectorizedFunction(yold)

	X = Xold[ynew != 0, :]
	y = ynew[ynew != 0]
	io.dump_svmlight_file(X, y, f2)
	return


if __name__ == '__main__':
	switch = sys.argv[1]
	infile = sys.argv[2]
	outfile = sys.argv[3]

	if switch == 'AvsI':
		labelFunction = AvsI
	if switch == 'AMvsI':
		labelFunction = AMvsI
	if switch == 'AvsMI':
		labelFunction = AvsMI

	changeSparseLabels(infile, outfile, labelFunction)