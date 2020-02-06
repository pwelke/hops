#!/usr/bin/env python2

'''
Transform a tid file from fsg (read from stdin) into a libsvm-format file.
Obtain graph labels from GRAPHDB (in the fsg input format)

usage: ./fsgtid2libsvm.py TIDFILE GRAPHDB OUTPUT

'''

import sys
import numpy as np
import scipy.sparse as sp
import svmlight_loader as io


def getTransactionLabels(f):
	labelList = list()
	for line in f:
		if (line.startswith('t')):
			labelList.append(int(line.split()[3])) # should be: t # id label n m
	return np.array(labelList)


def tidSparseLoader(f, n_transactions):
	pid = 0
	pattern_indices = list()
	transaction_indices = list()
	for line in f:
		tids = line.split()[1:]
		for tid in tids:
			pattern_indices.append(pid)
			transaction_indices.append(tid)
		pid += 1

	pids = np.array(pattern_indices, dtype=np.int64)
	tids = np.array(transaction_indices, dtype=np.int64)
	data = np.ones(tids.shape)

	return sp.csr_matrix((data, (tids, pids)), shape=(n_transactions, pid))


def tidSparseLoader2(f, n_transactions):

	# count elements and create arrays to hold them
	patternFile = open(f, 'r')
	elements = 0
	for line in patternFile:
		elements += len(line.split()) - 1
	patternFile.close()
	pids = np.zeros(elements, dtype=np.int64)
	tids = np.zeros(elements, dtype=np.int64)
	data = np.ones(elements, dtype=np.int)

	# fill arrays with values
	patternFile = open(f, 'r')
	i = 0
	pid = 0
	maxtid = 0
	for line in patternFile:
		localtids = line.split()[1:]
		# print(tids)
		for tid in localtids:
			tids[i] = tid
			pids[i] = pid
			maxtid = max(maxtid, tid)
			# print(str(i) + ' : ' + str(tids[i]))
			i += 1
		pid += 1
	patternFile.close()

	# print(n_transactions)
	# print(pid)
	# print(maxtid)

	return sp.csr_matrix((data, (tids, pids)), shape=(n_transactions, pid))

if __name__ == '__main__':
	if len(sys.argv) != 4:
		sys.stderr.write('fsgtid2libsvm: Error, wrong number of arguments: ' + str(len(sys.argv) - 1) + ' (expected: 3)')

	transactionFile = open(sys.argv[2], 'r')
	labels = getTransactionLabels(transactionFile)
	transactionFile.close()

	# novel variant that reduces memory usage
	data = tidSparseLoader2(sys.argv[1], labels.shape[0])

	# patternFile = open(sys.argv[1], 'r')
	# data = tidSparseLoader(patternFile, labels.shape[0])
	# patternFile.close()

	io.dump_svmlight_file(data, labels, sys.argv[3])
