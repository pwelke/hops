#!/usr/bin/env python2

'''Legacy code. Deprecated.

Use ../features/fsgtid2libsvm.py instead
'''

import sys

def grabLabels(f):
	labelList = list()
	for line in f:
		if (line.startswith('t')):
			labelList.append(line.split()) # should be: t # id label n m
	return labelList


def converter(f, labelList):
	pidMap = dict()
	pid = 1

	for line in f:
		ids = line.split()[1:]
		for i in ids:
			sys.stdout.write(labelList[int(i)][2] + ' ' + str(pid) + '\n')
		pid = pid + 1
	return pid


if __name__ == '__main__':
	transactionFile = open(sys.argv[1], 'r')
	labelList = grabLabels(transactionFile)
	pid = converter(sys.stdin, labelList)
	features = open(sys.argv[1] + '.features', 'w')
	for i in range(1, pid):
		features.write(str(i) + '\n')

