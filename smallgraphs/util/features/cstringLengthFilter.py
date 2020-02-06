#!/usr/bin/env python2

'''For a list of canonical strings in my format, return a
0/1 array indicating whether |E(P_i)| <= S.

usage: ./cstringLengthFilter.py S < FILE > OUTPUT

'''

import sys

# The number of opening brackets in the canonical stringis equal
# to the number of edges in the tree.
def filter_line(line, S, out):
	if int(line.count('(')) <= S:
		out.write('1\n')
	else:
		out.write('0\n')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write("fsgFeatureSelection.py: Takes exactly one argument\n")
		sys.exit(1)
		
	S = int(sys.argv[1]) - 1
	for line in sys.stdin:
		filter_line(line, S, sys.stdout)