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
  for n in range(init,end+1):
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
  for n in range(init,end+1):
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
