#!/usr/bin/env python2

'''
Given a file with arbitrary items, separated by spaces and possibly on multiple lines, 
map those labels to the range [1,n] where n is the number of distinct labels in the file.

Numbers are given in the order of first appearance in the file and if a label occurs more
than once it is always mapped to the same number.

The line structure of the file is kept intact. 

Written by Pascal Welke 2017-01-27

usage: edgeListDensification.py < IN > out
'''

import sys

mapping = dict()
currentInt = 1

def getMapping(label):
	global mapping
	global currentInt

	try:
		return mapping[label]
	except Exception as e:
		currentString = str(currentInt)
		mapping[label] = currentString
		currentInt += 1
		return currentString


if __name__ == '__main__':

	for line in sys.stdin:
		labels = line.split()
		newlabels = [getMapping(x) for x in labels]
		sys.stdout.write(' '.join(newlabels))
		sys.stdout.write('\n')
