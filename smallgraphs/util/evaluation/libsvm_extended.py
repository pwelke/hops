#!/usr/bin/env python2

from operator import itemgetter
from sklearn import cross_validation
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as pl
import numpy as np
import svmutil


def auc(deci, label):
    #count of positive and negative labels
    db = []
    pos, neg = 0, 0

    for i in range(len(label)):
        if label[i]>0:
            pos+=1
        else:
            neg+=1
        db.append([deci[i], label[i]])

    #sorting by decision value
    db = sorted(db, key=itemgetter(0), reverse=True)

    #calculate ROC 
    xy_arr = []
    tp, fp = 0., 0. #assure float division
    for i in range(len(db)):
        if db[i][1]>0:
            tp+=1
        else:
            fp+=1
        xy_arr.append([fp/neg,tp/pos])

    #area under curve
    aoc = 0.
    prev_x = 0
    for x,y in xy_arr:
        if x != prev_x:
            aoc += (x - prev_x) * y
            prev_x = x
    return aoc

def plot_roc(deci, label):
    #count of positive and negative labels
    db = []
    pos, neg = 0, 0

    for i in range(len(label)):
        if label[i]>0:
            pos+=1
        else:
            neg+=1
        db.append([deci[i], label[i]])

    #sorting by decision value
    db = sorted(db, key=itemgetter(0), reverse=True)

    #calculate ROC 
    xy_arr = np.zeros([len(deci), 2])
    tp, fp = 0., 0. #assure float division
    for i in range(len(db)):
        if db[i][1]>0:
            tp+=1
        else:
            fp+=1
        xy_arr[i,0] = fp/neg
        xy_arr[i,1] = tp/pos

    #area under curve
    aoc = 0.
    prev_x = 0
    for x,y in xy_arr:
        if x != prev_x:
            aoc += (x - prev_x) * y
            prev_x = x
            
    #begin plot
    pl.figure()
    pl.xlabel = ('False Positive Rate')
    pl.ylabel = ('True Positive Rate')
    pl.title = ('ROC curve  (AUC = %.4f)' % (aoc))
    pl.plot(xy_arr[:,0],xy_arr[:,1])
    pl.show()

    return aoc

# from http://stackoverflow.com/questions/34371994/libsvms-python-binding-and-cross-validation-with-precomputed-kernel
# with changes motivated by http://stackoverflow.com/questions/10978261/libsvm-precomputed-kernels
def compute_accuracy(gram_matrix, data, k=10):

    kv = cross_validation.StratifiedKFold(labels, n_folds=k)
    s = 0.0

    for train_index, test_index in kv:

        gm_train = gram_matrix[train_index, :]
        gm_train = gm_train[:, train_index]
        data_train = data[train_index]

        # libSVM wants the distances from test instances to all train instances as input
        # see http://stackoverflow.com/questions/10978261/libsvm-precomputed-kernels
        gm_test = gram_matrix[test_index, :]
        gm_test = gm_test[:, train_index] #!
        data_test = data[test_index]

        # Have to use libsvm directly here, because of a bug in sklearn with precomputed gram matrices
        x = []
        for i in range(len(gm_train)):
            l = gm_train[i].tolist()
            l.insert(0, i + 1)
            x.append(l)

        prob = svmutil.svm_problem(data_train.tolist(), x, isKernel=True)
        param = svmutil.svm_parameter('-t 4 -c 10 -q')
        m = svmutil.svm_train(prob, param)

        xx = []
        for i in range(len(gm_test)):
            t = gm_test[i].tolist()
            t.insert(0, i + 1)
            xx.append(t)

        p_label, p_acc, p_val = svmutil.svm_predict(data_test.tolist(), xx, m)

        ACC, MSE, SCC = evaluations(p_label, data_test.tolist())
        s += ACC

    return s / k

def compute_auc(gram_matrix, data, k=10, C=1.0):

    kv = cross_validation.StratifiedKFold(labels, n_folds=k)
    s = 0.0

    for train_index, test_index in kv:

        gm_train = gram_matrix[train_index, :]
        gm_train = gm_train[:, train_index]
        data_train = data[train_index]

        # libSVM wants the distances from test instances to all train instances as input
        # see http://stackoverflow.com/questions/10978261/libsvm-precomputed-kernels
        gm_test = gram_matrix[test_index, :]
        gm_test = gm_test[:, train_index] #!
        data_test = data[test_index]

        # Have to use libsvm directly here, because of a bug in sklearn with precomputed gram matrices
        x = []
        for i in range(len(gm_train)):
            l = gm_train[i].tolist()
            l.insert(0, i + 1)
            x.append(l)

        prob = svmutil.svm_problem(data_train.tolist(), x, isKernel=True)
        param = svmutil.svm_parameter("-t 4 -c %.410f -q" % C)
        m = svmutil.svm_train(prob, param)

        xx = []
        for i in range(len(gm_test)):
            t = gm_test[i].tolist()
            t.insert(0, i + 1)
            xx.append(t)

        p_label, p_acc, p_val = svmutil.svm_predict(data_test.tolist(), xx, m)

        fpr, tpr, thresholds = roc_curve(data_test, p_val, pos_label=1.0)
        AUC = roc_auc_score(data_test, p_val)
        s += AUC

    return s / k

def compute_auc_kern(data, labels, k=10, C=1.0, kern=6, gamma=None):
    ''' This is an interface to the extended libsvm implementation
    with new kernels '''

    kv = cross_validation.StratifiedKFold(labels, n_folds=k, random_state=1)
    s = 0.0

    for train_index, test_index in kv:

        data_train = data[train_index]
        labels_train = labels[train_index]

        data_test = data[test_index]
        labels_test = labels[test_index]

        y_train = labels_train.tolist()
        x_train = data_train.tolist()
        
        prob = svmutil.svm_problem(y_train, x_train)
        if gamma != None:
        	param = svmutil.svm_parameter("-t %i -c %.410f -q -g %i" % (kern, C, gamma))
        else:
        	param = svmutil.svm_parameter("-t %i -c %.410f -q" % (kern, C))

        model = svmutil.svm_train(prob, param)

        y_test = labels_test.tolist()
        x_test = data_test.tolist()
        
        p_label, p_acc, p_val = svmutil.svm_predict(y_test, x_test, m=model)

        fpr, tpr, thresholds = roc_curve(labels_test, p_val, pos_label=-1.0)
        AUC = roc_auc_score(labels_test, p_val)
        s += AUC

    return s / k

import itertools
def sparseMatrix2dict(X):
    Xcoo = X.tocoo()
    Xdicts = [dict() for _ in xrange(Xcoo.shape[0])]
    for i,j,v in itertools.izip(Xcoo.row, Xcoo.col, Xcoo.data):
        Xdicts[i][j] = v
    return Xdicts

def compute_auc_kern_sparse(data, labels, k=10, C=1.0, kern=6, gamma=None):
    ''' This is an interface to the extended libsvm implementation
    with new kernels '''

    kv = cross_validation.StratifiedKFold(labels, n_folds=k, random_state=1)
    s = 0.0

    for train_index, test_index in kv:
    	# training
        data_train = data[train_index, :]
        labels_train = labels[train_index]

        x_train = sparseMatrix2dict(data_train)

        prob = svmutil.svm_problem(labels_train, x_train)
        if gamma != None:
        	param = svmutil.svm_parameter("-t %i -c %.410f -q -g %i" % (kern, C, gamma))
        else:
        	param = svmutil.svm_parameter("-t %i -c %.410f -q" % (kern, C))

        model = svmutil.svm_train(prob, param)
        
        # testing
        data_test = data[test_index, :]
        labels_test = labels[test_index]

        x_test = sparseMatrix2dict(data_test)

        p_label, p_acc, p_val = svmutil.svm_predict(labels_test, x_test, m=model)

        fpr, tpr, thresholds = roc_curve(labels_test, p_val, pos_label=-1.0)
        AUC = roc_auc_score(labels_test, p_val)
        s += AUC

    return s / k


# import itertools 

# def compare(X, y):
# 	probs = svmutil.svm_problem_sparse(y, X)
# 	probd = svmutil.svm_problem(y, X.toarray().tolist())

# 	print 'sparse:'
# 	print probs
# 	print probs.l
# 	print probs.n
# 	print len(probs.x)
# 	# for i, yi in enumerate(probs.x): print probs.x[i]
# 	print len(probs.y)
# 	# for i, yi in enumerate(probs.y): print probs.y[i]
# 	print 'dense:'
# 	print probd
# 	print probd.l
# 	print probd.n
# 	print len(probd.x)
# 	# for i, yi in enumerate(probd.x): print probd.x[i]
# 	print len(probd.y)
# 	# for i, yi in enumerate(probd.y): print probd.y[i]

# 	# xdiff = 0
# 	# ydiff = 0
# 	# for xd, xs in itertools.izip_longest(probd.x, probs.x, fillvalue=None):
# 	# 	if xd != xs:
# 	# 		xdiff += 1
# 	# for yd, ys in itertools.izip_longest(probd.y, probs.y, fillvalue=None):
# 	# 	if yd != ys:
# 	# 		ydiff += 1

# 	# print 'xdiff ' + str(xdiff)
# 	# print 'ydiff ' + str(ydiff)