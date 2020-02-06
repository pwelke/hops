#!/usr/bin/env python2

'''Transform an sdf file containing a bunch of molecules to the format needed by 
my cyclic pattern kernel / graph mining suite.

The sdf input format can be exchanged by any format that is spoken by openbabel
( http://openbabel.org )

Accepts either 2, 1 or zero arguments. Usage

sdf2aids INFILE OUTFILE
sdf2aids INFILE
sdf2aids

in the second case, output is written to stdout
in the third case, input is read from stdin and output is written to stdout

2014-03-27 pwelke'''

from openbabel import *
import sys

if len(sys.argv) <= 2:
	outfile = sys.stdout
	if len(sys.argv) == 1:
		infile = sys.stdin
	else:
		infile = sys.argv[1]
else:
	outfile = open(sys.argv[2], 'w')

# read sdf
molid = 1
obconversion = OBConversion()
obconversion.SetInFormat("sdf")
obmol = OBMol()

notDone = obconversion.ReadFile(obmol, infile)
while notDone:
	outfile.write(' '.join(['#', str(molid), '0', str(obmol.NumAtoms()), str(obmol.NumBonds())]))
	outfile.write('\n')
	obmol_atomiter = OBMolAtomIter(obmol)
	obmol_bonditer = OBMolBondIter(obmol)

	for atom in obmol_atomiter:
		outfile.write(str(atom.GetAtomicNum()) + ' ')
	outfile.write('\n')

	for bond in obmol_bonditer:
		outfile.write(str(bond.GetBeginAtomIdx()) + ' ' + str(bond.GetEndAtomIdx()) + ' ' + str(bond.GetBondOrder()) + ' ')
	outfile.write('\n')

	obmol = OBMol()
	notDone 	= obconversion.Read(obmol)
	molid += 1

outfile.write('$\n')
outfile.close()