#!/usr/bin/env python2

from math import sqrt
import sys

def mean(l):
	m = 0.0
	for value in l:
		m += value
	return m / len(l)

def std(l, m):
	s = 0.0
	for value in l:
		s = s + (m - value) * (m - value)
	s = s / len(l)
	return sqrt(s)

def readList(f):
	l = list()
	for line in f:
		l.append(float(line))
	return l

if __name__ == '__main__':
	if len(sys.argv) == 1:
		l = readList(sys.stdin)
		if len(l) == 0:
			sys.stdout.write('NORESULTS\n')
		else:
			m = mean(l)
			s = std(l, m)
			sys.stdout.write("{0:.2f}\n".format(m))
	else:
		for f in range(1, len(sys.argv)):
			fo = open(sys.argv[f])
			l = readList(fo)
			fo.close()
			if len(l) == 0:
				sys.stdout.write(sys.argv[f] + '\tNORESULTS\n')
			else:
				m = mean(l)
				s = std(l, m)
				sys.stdout.write(sys.argv[f] + "\t{0:.2f}\n".format(m))

