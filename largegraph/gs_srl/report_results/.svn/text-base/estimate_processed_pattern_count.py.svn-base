'''
Created on Jul 12, 2017

@author: irma
'''
import argparse,os
import numpy as np

def get_batch_paths(path_results):
    tmp=[]
    for dir in os.listdir(path_results):
        if dir.startswith("batch"):
          tmp.append(dir)
    return tmp  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r',help='path to results for a dataset')
    args = parser.parse_args()
    count=0
    lengths=[]
    for pat in os.listdir(args.r):
        print pat
        if "patterns size " in pat.replace("_"," ") and not "init" in pat.replace("_"," "):
            #count batches
            
            batches=get_batch_paths(os.path.join(args.r,pat))
            print pat,"batches #=",len(batches)
            lengths.append(len(batches))
            count+=len(batches)*400
    print "Estimated nr patterns = ",count
    print "Average nr batches: ",np.mean(lengths)