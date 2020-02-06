#!/usr/bin/env python2

import sys

'''Transform a transaction database from our format into the format expected by fsg.
Reads from stdin and writes to stdout.'''

def aidsGraph2fsg(header, vertices, edges, out):
	out.write('t ' + header)
	vlabels = vertices.strip().split(' ')
	for v in range(len(vlabels)):
		out.write(' '.join(['v', str(v), vlabels[v], '\n']))
	es = edges.strip().split(' ')
	if len(es) >= 3:
		for e in range(0, len(es), 3):
			out.write(' '.join(['u', str(int(es[e])-1), str(int(es[e+1])-1), es[e+2], '\n']))

if __name__ == '__main__':
	inp = sys.stdin
	out = sys.stdout

	header = inp.readline()
	while header.startswith('$') != True:
		vertices = inp.readline()
		edges = inp.readline()
		aidsGraph2fsg(header, vertices, edges, out)
		header = inp.readline()
