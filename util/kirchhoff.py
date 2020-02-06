#!/usr/bin/env python2
from numpy.linalg import det
from numpy import *

import sys

''' Read a graph db in aids format and print the graph identifier and the number of spanning trees to stdout.
Spanning trees are computed using Kirchhoffs matrix tree theorem '''


def computeCofactor(laplacian):
	subl = laplacian[:-1,:-1]
	nTrees = det(subl)
	return nTrees

def createLaplacian(line, n):
	laplacian = zeros([n,n])
	i=0
	tokens = line.split()
	while i < len(tokens):
		v = int(tokens[i]) - 1
		w = int(tokens[i+1]) - 1
		laplacian[v,w] = -1.0
		laplacian[w,v] = -1.0
		i = i + 3
	for i in range(n):
		laplacian[i,i] = -laplacian[i,:].sum()
	return laplacian


# inclusion / exclusion (particularly, exclusion) tells us that
# the number of spanning trees containing an edge are all spanning 
# trees minus the ones that do not contain the edge. 
# This is what is computed here
def computeEdgeRemovalNSpanningTrees(laplacian, line):
	tokens = line.split()
	spts = zeros([len(tokens) / 3, 1])
	i = 0
	while i < len(tokens):
		v = int(tokens[i]) - 1
		w = int(tokens[i+1]) - 1
		laplacian[v,w] = 0.0
		laplacian[w,v] = 0.0
		laplacian[v,v] = laplacian[v,v] - 1.0
		laplacian[w,w] = laplacian[w,w] - 1.0

		spts[i/3, 0] = computeCofactor(laplacian)

		laplacian[v,w] = -1.0
		laplacian[w,v] = -1.0
		laplacian[v,v] = laplacian[v,v] + 1.0
		laplacian[w,w] = laplacian[w,w] + 1.0

		i = i + 3

	return spts


# compute the probability that a spanning tree taken uniformly at random
# contains edge e for each edge in the graph.
def computeFractions(nTrees, nRemovalTrees):
	nTrees.round()
	nRemovalTrees.round()
	fractions = ones(nRemovalTrees.shape) - (1.0 / nTrees) * nRemovalTrees
	return fractions

def printArray(array):
	s = ''
	for i in array[0]:
		s = s + ' ' + str(i)
	return s


def printEdgeRemovalNSpanningTrees(f):
	for line in f:
		if line[0] == '#':
			tokens = line.split()
			graphno = tokens[1]
			n = int(tokens[3])
			m = int(tokens[4])
			edges = f.next()
			edges = f.next()

			laplacian = createLaplacian(edges, n)
			nTrees = computeCofactor(laplacian)
			nRemovalTrees = computeEdgeRemovalNSpanningTrees(laplacian, edges)
			# suppress scientific notation for integer number of spanning trees 
			print graphno + " " + str(int(nTrees)) + printArray(computeFractions(nTrees,nRemovalTrees).T)
	


def printNSpanningTrees(f):
	for line in f:
		if line[0] == '#':
			tokens = line.split()
			graphno = tokens[1]
			n = int(tokens[3])
			m = int(tokens[4])
			edges = f.next()
			edges = f.next()

			laplacian = createLaplacian(edges, n)
			nTrees = computeCofactor(laplacian)
			print graphno + " " + str(nTrees)
	
def main():
	if len(sys.argv) == 2:
		f = open(sys.argv[1])
	else:
		f = sys.stdin

	printEdgeRemovalNSpanningTrees(f)
	f.close()

if __name__ == '__main__':		
	main()

