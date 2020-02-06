#!/usr/bin/env python2

import sys


def isComment(line):
	return line.startswith('#')

def isTransaction(line):
	return line.startswith('t')

def isVertex(line):
	return line.startswith('v')

def isEdge(line):
	return line.startswith('e')

def isNumber(token):
	try:
		int(token)
		return True
	except Exception as e:
		return False


def isFrequencyCount(line):
	split = line.split(' ')
	return line.startswith('# ') & isNumber(split[1])

def printGraph(i, activity, vertexList, edgeList, out):
	if len(vertexList) == 0:
		return
	out.write('# ' + str(i) + ' ' + str(activity) + ' ' + str(len(vertexList)) + ' ' + str(len(edgeList)) + '\n')
	# TODO: sort and check if vertex indices are correctly ordered
	for v in vertexList:
		out.write(v[1] + ' ')
	out.write('\n')
	for e in edgeList:
		out.write(str(int(e[0])+1) + ' ' + str(int(e[1])+1) + ' ' + e[2] + ' ')
	out.write('\n')

def parseFile(f, out):
	id = -1
	activity = 0
	edgeList = list()
	vertexList = list()
	for line in f:
		if isFrequencyCount(line):
			printGraph(id, activity, vertexList, edgeList, out) # print previous! graph
			vertexList = list()
			edgeList = list()
			activity = int(line.split(' ')[1])
		if isVertex(line):
			vertexList.append(line.split()[1:3])
		if isEdge(line):
			edge = line.split()
			edgeList.append(edge[1:4])
		if isTransaction(line):
			# obtain transaction id
			id = int(line.split(' ')[1])
	printGraph(id, activity, vertexList, edgeList, out) # print last graph
	out.write('$\n')

if __name__ == '__main__':
	if len(sys.argv) > 3:
		sys.stderr.write('gaston2aids.py: too many arguments.\n')
	if len(sys.argv) == 2:
		f = open(sys.argv[1], 'r')
		g = open(sys.argv[2], 'w')
		parseFile(f, g)
		f.close()
		g.close()
	if len(sys.argv) == 2:
		f = open(sys.argv[1], 'r')
		parseFile(f, sys.stdout)
		f.close()
	if len(sys.argv) == 1:
		parseFile(sys.stdin, sys.stdout)

			