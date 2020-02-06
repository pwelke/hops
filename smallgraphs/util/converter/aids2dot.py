#!/usr/bin/env python2

import sys

def aids2dotLabeledSingleGraph(f, out):
	# print graph header
	out.write('graph combination {\n')
	for line in f:
		if line[0] == '#':
			graphDescription = line.split()
			vertices = f.next()
			vertexLabels = vertices.split()
			edges = f.next()
			edgeDescriptions = edges.split()
			
			graphno = graphDescription[1]
			n = int(graphDescription[3])
			m = int(graphDescription[4])

			# write vertices with labels
			for i in range(len(vertexLabels)):
				out.write('g' + graphno + '_v' + str(i+1) + ' [label=' + vertexLabels[i] + '];\n')

			# write edges with labels
			for i in range(0, len(edgeDescriptions), 3):
				out.write('g' + graphno + '_v' + edgeDescriptions[i] + ' -- ' + 'g' + graphno + '_v' + edgeDescriptions[i+1] + ' [label=' + edgeDescriptions[i+2] + '];\n')

	# terminate graph description
	out.write('}\n')

def aids2dotLabeled(f, out):
	for line in f:
		if line[0] == '#':
			graphDescription = line.split()
			vertices = f.next()
			vertexLabels = vertices.split()
			edges = f.next()
			edgeDescriptions = edges.split()
			
			graphno = graphDescription[1]
			n = int(graphDescription[3])
			m = int(graphDescription[4])

			# print graph header
			out.write('graph ' + graphno + ' {\n')

			# write vertices with labels
			for i in range(len(vertexLabels)):
				out.write(str(i+1) + ' [label=' + vertexLabels[i] + '];\n')

			# write edges with labels
			for i in range(0, len(edgeDescriptions), 3):
				out.write(edgeDescriptions[i] + ' -- ' + edgeDescriptions[i+1] + ' [label=' + edgeDescriptions[i+2] + '];\n')

			# terminate graph description
			out.write('}\n')

def aids2dotUnlabeledStartingWith1(f, out):
	for line in f:
		if line[0] == '#':
			graphDescription = line.split()
			vertices = f.next()
			vertexLabels = vertices.split()
			edges = f.next()
			edgeDescriptions = edges.split()
			
			graphno = graphDescription[1]
			n = int(graphDescription[3])
			m = int(graphDescription[4])

			# print graph header
			out.write('graph ' + graphno + ' {\n')

			# write vertices with labels
			for i in range(len(vertexLabels)):
				out.write(str(i+1) + ';\n')

			# write edges without labels
			for i in range(0, len(edgeDescriptions), 3):
				out.write(edgeDescriptions[i] + ' -- ' + edgeDescriptions[i+1] + ';\n')

			# terminate graph description
			out.write('}\n\n')


def aids2dotUnlabeledStartingWith0(f, out):
	for line in f:
		if line[0] == '#':
			graphDescription = line.split()
			vertices = f.next()
			vertexLabels = vertices.split()
			edges = f.next()
			edgeDescriptions = edges.split()
			
			graphno = graphDescription[1]
			n = int(graphDescription[3])
			m = int(graphDescription[4])

			# print graph header
			out.write('graph ' + graphno + ' {\n')

			# write vertices with labels
			for i in range(len(vertexLabels)):
				out.write(str(i+1) + ' [label=' + str(i) + '];\n')

			# write edges without labels
			for i in range(0, len(edgeDescriptions), 3):
				out.write(edgeDescriptions[i] + ' -- ' + edgeDescriptions[i+1] + ';\n')

			# terminate graph description
			out.write('}\n\n')

if __name__ == '__main__':
	# defaults
	function = aids2dotLabeled
	f = sys.stdin

	# input handling
	if len(sys.argv) >= 2:
		if sys.argv[1].startswith('-'):
			if (sys.argv[1] == '-sl') | (sys.argv[1] == '-singleLabeled'):
				function = aids2dotLabeledSingleGraph
			if (sys.argv[1] == '-l'):
				function = aids2dotLabeled
			if (sys.argv[1] == '-0'):
				function = aids2dotUnlabeledStartingWith0
			if (sys.argv[1] == '-1') | (sys.argv[1] == '-unlabeled'):
				function = aids2dotUnlabeledStartingWith1

			if len(sys.argv) >= 3:
				f = open(sys.argv[2])
		else:
			f = open(sys.argv[1])

	# work
	function(f, sys.stdout)
	f.close()