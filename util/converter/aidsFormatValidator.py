#!/usr/bin/env python2

import sys

def validate(header, vertices, edges, out):
	hd = header.strip().split(' ')
	if (len(hd) != 5):
		sys.stderr.write("Invalid header1: " + header + "\n")
		return False
	if not header.startswith('#'):
		sys.stderr.write("Invalid header2: " + header + "\n")
		return False
	try:
		number = int(hd[1])
		activity = int(hd[2])
		n = int(hd[3])
		m = int(hd[4])
	except ValueError:
		sys.stderr.write("Invalid header3: " + header + "\n")
		return False
	
	vs = vertices.strip().split(' ')
	if len(vs) != n:
		if (len(vs)==1 & vs[0]=='' & n==0): # funny case: ' \n'.strip().split(' ') returns ['']
			pass
		else:
			sys.stderr.write("Invalid number of vertex labels: " + str(len(vs)) + "for graph " + header + "\n")
			return False

	es = edges.strip().split(' ')
	if len(es) != 3 * m:
		if (len(vs)==1 & vs[0]=='' & n==0): # funny case: ' \n'.strip().split(' ') returns ['']
			pass
		else:
			sys.stderr.write("Invalid number of descriptors: " + str(len(es)) + " (should be " + str(m * 3) + ") for graph " + header + "\n")
			return False
	try:
		i = 0
		while (i < len(es)):
			v = int(es[i])
			w = int(es[i+1])
			if (v < 1) or (v > n) or (w < 1) or (w > n):
				sys.stderr.write("Invalid edge descriptor: " + es[i] + ' ' + es[i+1] + ' ' + es[i+2] + "for graph " + header + '\n') 
				return False
			i += 3
	except ValueError:
		sys.stderr.write("Invalid edge descriptor: " + es[i] + ' ' + es[i+1] + ' ' + es[i+2] + "for graph " + header + '\n') 
		return False
	return True


def offsetEdges(header, vertices, edges, out):
	hd = header.strip().split()
	number = int(hd[1])
	activity = int(hd[2])
	n = int(hd[3])
	m = int(hd[4])
	sys.stdout.write(header)
	sys.stdout.write(vertices)

	es = edges.strip().split()
	i = 0
	while (i < len(es)):
		v = int(es[i]) + 1
		w = int(es[i+1]) + 1
		if (v < 1) or (v > n) or (w < 1) or (w > n):
			sys.stderr.write("Invalid edge descriptor: " + es[i] + ' ' + es[i+1] + ' ' + es[i+2] + "for graph " + header + '\n') 
			return False
		sys.stdout.write(str(v) + ' ' + str(w) + ' ' + es[i+2] + ' ')
		i += 3
	sys.stdout.write('\n')


# if __name__ == '__main__':
# 	inp = sys.stdin
# 	out = sys.stdout

# 	header = inp.readline()
# 	while header.startswith('$') != True:
# 		vertices = inp.readline()
# 		edges = inp.readline()
# 		validate(header, vertices, edges, out)
# 		header = inp.readline()
 
if __name__ == '__main__':
	inp = sys.stdin
	out = sys.stdout

	header = inp.readline()
	while header.startswith('$') != True:
		vertices = inp.readline()
		edges = inp.readline()
		validate(header, vertices, edges, out)
		header = inp.readline()
	sys.stdout.write('$\n')