#!/usr/bin/env python2

'''Select tid lists of all patterns P with |V(P)| <= S.

usage: ./fsgFeatureSelector.py S < FILE > OUTPUT

'''

import sys

# Each line in a .tid file produced by fsg starts with x-y where x denotes the number of edges in the pattern
# and y denotes the id of the pattern. We output those lines that have x <= S.
def filter(line, S, out):
  if int(line.split('-')[0]) <= S:
    out.write(line)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.stderr.write("fsgFeatureSelection.py: Takes exactly one argument\n")
  else:
    S = int(sys.argv[1])
    for line in sys.stdin:
      filter(line, S, sys.stdout)