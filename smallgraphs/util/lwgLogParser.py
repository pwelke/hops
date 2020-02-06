#!/bin/env python3

import sys
from collections import Counter

keywords = ['generated', 'unique', 'apriori', 'intersection', 'frequent']
longestKeyword = max([len(k) for k in keywords])
times = ['real', 'user', 'sys']

def offset(keyword):
	return ' ' * (longestKeyword - len(keyword) + 1)

def timeconverter(ugly):
	resultingSec = 0.0
	# ugly may be something like 8m9,585s
	
	hours = ugly.split('h')
	if len(hours) > 1:
		resultingSec += int(hours[0]) * 3600.0
		ugly = ''.join(hours[1:])
	
	minutes = ugly.split('m')
	if len(minutes) > 1:
		resultingSec += int(minutes[0]) * 60.0
		ugly = ''.join(minutes[1:])
	seconds = ugly.replace(',','.')[:-1]
	resultingSec += float(seconds)
	return resultingSec

def parseLWGErr(f):
	d = dict()
	t = dict()
	patternsize = 0
	for line in f:
		if line.startswith('Processing patterns with '):
			patternsize = int(line.split(' ')[3])
			d[patternsize] = dict()
		for keyword in keywords:
			if line.startswith(keyword):
				d[patternsize][keyword] = int(line.split(' ')[-1])
		for time in times:
			if line.startswith(time):
				t[time] = timeconverter(line.split()[-1])		

	return d, t	

def report(d, t):
	sums = Counter()
	for psize in d.keys():
		for keyword in keywords:
			sums[keyword] += d[psize][keyword]

	time = times[1]
	print('time in seconds: ' + str(t[time]))
	for keyword in keywords:
		print(keyword + ' patterns per second:' + offset(keyword) + str(sums[keyword] / t[time]))



if __name__ == '__main__':
	d, t = parseLWGErr(sys.stdin)
	report(d, t)