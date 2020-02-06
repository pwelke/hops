#!/usr/bin/env python2
#This tool allow users to plot SVM-prob ROC curve from data
from svmutil import *
from sys import argv, platform
from os import path, popen
from random import randrange , seed
from operator import itemgetter
from time import sleep

''' Assumptions:
deci: an array of floats containing decision values. The smallest number corresponds to the 
'most negative' prediction, the largest number to the 'most positive' prediction, where the 
'negative' class is the class with label <= 0, the positive class the class with label > 0.
label: an array of floats containing the ground truth. Positive examples have a value > 0, negative
examples have a value <= 0. '''

def sortByDecisionValue(deci, label):
	#count of positive and negative labels
	db = []
	# pos, neg = 0, 0 		
	for i in range(len(label)):
		# if label[i]>0:
		# 	pos+=1
		# else:	
		# 	neg+=1
		db.append([deci[i], label[i]])

	#sorting by decision value
	db = sorted(db, key=itemgetter(0), reverse=True)
	return db

def compute_precisionAtK(deci, label, k):
	db = sortByDecisionValue(deci, label)
	precision = 0.0
	for i in range(k):
		# prediction is correct if product of prediction and
		# label is positive (same signum), except in case 
		# both are 0, which is caught by the second check. 
		if (db[i][0] * db[i][1] > 0) || (db[i][0] == db[i][1]):
			precision += 1.0
	return precision / k
  

# Compute ROC curve from deci and label
def compute_roc(deci, label):

	db = sortByDecisionValue(deci, label)

	#calculate ROC 
	xy_arr = []
	tp, fp = 0., 0.			#assure float division
	for i in range(len(db)):
		if db[i][1]>0:		#positive
			tp+=1
		else:
			fp+=1
		xy_arr.append([fp/neg,tp/pos])
	return xy_arr

# area under curve
def compute_auc(xy_arr):
	auc = 0.			
	prev_x = 0
	for x,y in xy_arr:
		if x != prev_x:
			auc += (x - prev_x) * y
			prev_x = x
	return auc


def plot_roc(deci, label, output, title, params):
	xy_arr = compute_roc(deci, label)
	try:
		#begin gnuplot
		if title == None:
			title = output
		#also write to file
		g = gnuplot(output)
		g.xlabel = "False Positive Rate"
		g.ylabel = "True Positive Rate"
		g.title = "ROC curve of %s \\n (AUC = %.4f) parameters: %s" % (title, aoc, params)
		g.plotline(xy_arr)
	except Exception, e:
		print e
	
	return compute_auc(xy_arr)