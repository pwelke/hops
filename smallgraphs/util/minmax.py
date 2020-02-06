#!/usr/bin/env python2

import sys

maxi = -1
mini = -1
for line in sys.stdin:
	x = [int(i) for i in line.split()]
	maxx = max(x)
	minx = min(x)
	if maxi < maxx:
		maxi = maxx
	if (mini > minx) | (mini == -1):
		mini = minx

print 'min = ' + str(mini)
print 'max = ' + str(maxi)
