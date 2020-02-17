'''
Created on Jan 17, 2016

@author: irma
'''
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def collect_all_degrees(path_to_csvs,init,end):
  array_embeddings=[]
  for n in xrange(init,end+1):
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        with open(path_to_exhaustive_csv) as exh:
            reader = csv.DictReader(exh)
            for row in reader:
               if(not(row["max_degree"])):
                   continue
               array_embeddings.append(float(row["max_degree"]))
  return array_embeddings

def collect_all_embeddings_exhaustive(path_to_csvs,init,end):
  array_embeddings=[]
  for n in xrange(init,end+1):
        path_to_exhaustive_csv=path_to_csvs+"/exhaustive_"+str(n)+".csv"
        with open(path_to_exhaustive_csv) as exh:
            reader = csv.DictReader(exh)
            for row in reader:
               if(not(row["exh_emb"])):
                   continue
               array_embeddings.append(float(row["exh_emb"]))
  return array_embeddings
            

def discretize_array(raw_array,nr_categories,array_of_categories_name):
     return pd.qcut(raw_array, nr_categories, labels=array_of_categories_name)

if __name__ == '__main__':
    arrayExh=collect_all_embeddings_exhaustive("/home/irma/workspace/Martin_Experiment/RESULTS/RESULTS_DBLP/csvs/",4,4)
    print arrayExh
    arrayDiscretized,tercile=pd.qcut(np.array(arrayExh), 3,retbins=True, labels=["small","medium","large"])
    print "tercile: ",tercile
    #a = pd.DataFrame(columns=['data'])
    #a.data = arrayExh
    #print a
    #a[a > tercile].dropna()
    #print a
    againDiscretized= pd.cut(np.array([9908]),tercile,include_lowest=True,labels=["small","medium","large"])
    print "Before: ",arrayDiscretized
    print "After: ",againDiscretized
    
    #quantiles = np.linspace(0, 1, 3 + 1)
    #print quantiles
    #q, bins = pd.qcut(range(5),4, retbins=True)
    #print "q",q
    #print "bins",bins
    #b = np.array(range(5))
    #hist = pd.cut(b, bins,include_lowest=True,labels=["small","medium","large","whatevs"])
    #print "hist",hist 