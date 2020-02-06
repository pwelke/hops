#!/usr/bin/env python2
import sys

def printK_n(n, out):
	
	# write header
	m = n * (n - 1) / 2
	out.write('# ' + str(n) + ' 0 ' + str(n) + ' ' + str(m) + '\n')
	
	# write vertex labels
	for i in range(1, n+1):
		out.write('1 ')
	out.write('\n')

	# write edges
	for i in range(1, n+1):
		for j in range(i+1, n+1):
			out.write(str(i) + ' ' + str(j) + ' 1 ')
	out.write('\n')

def printTermination(out):
	out.write('$\n')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write('completeGraphGenerator.py: Invalid number of arguments\n')
	else:
		n = int(sys.argv[1])
		printK_n(n, sys.stdout)
		printTermination(sys.stdout)