#!/usr/bin/env python2

'''
Transform a tid file from lwg (read from stdin) into a libsvm-format file.
Obtain graph labels from GRAPHDB (in the aids input format)

usage: ./lwgtid2libsvm.py TIDFILE GRAPHDB OUTPUT

'''

import sys
import numpy as np
import scipy.sparse as sp
import svmlight_loader as io


def getTransactionLabelsAndDict(f):
	indexDict = dict()
	labelList = list()
	index = 0
	for line in f:
		if (line.startswith('#')):
			tokens = line.split()
			labelList.append(int(tokens[2])) # should be: # id label n m
			indexDict[tokens[1]] = index
			index += 1
	return (np.array(labelList), indexDict)


''' Converts the pattern_id transaction_id based output of lwg to a sparse array in csr_matrix format.

Note that lwg outputs the ids of transactions that are specified in the graph file, and not consecutive numbers from 0 to N-1.
We convert this (as well as the pattern ids) to consecutive numbers from 0 to N-1 (resp. P-1) where N is the size of the database 
and P is the size of the pattern set'''
def tidSparseLoader(f, n_transactions, indexDict):
	pattern_indices = list()
	transaction_indices = list()
	pid = 0
	for line in f:
		tokens = line.split() # format of line is pid: tid1 tid2 ...
		# pid = tokens[0][:-1] # pid without trailing colon
		tids = tokens[1:]

		for tid in tids:
			pattern_indices.append(pid)
			transaction_indices.append(indexDict[tid])
		pid += 1

	pids = np.array(pattern_indices, dtype=np.int64)
	tids = np.array(transaction_indices, dtype=np.int64)
	data = np.ones(tids.shape)

	return sp.csr_matrix((data, (tids, pids)), shape=(n_transactions, pid))


if __name__ == '__main__':
	if len(sys.argv) != 4:
		sys.stderr.write('fsgtid2libsvm: Error, wrong number of arguments: ' + str(len(sys.argv) - 1) + ' (expected: 3)')

	transactionFile = open(sys.argv[2], 'r')
	labels, indexDict = getTransactionLabelsAndDict(transactionFile)
	transactionFile.close()

	patternFile = open(sys.argv[1], 'r')
	data = tidSparseLoader(patternFile, labels.shape[0], indexDict)
	patternFile.close()

	io.dump_svmlight_file(data, labels, sys.argv[3])
