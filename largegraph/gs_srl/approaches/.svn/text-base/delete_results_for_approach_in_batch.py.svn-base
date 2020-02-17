'''
Created on May 5, 2015

@author: irma
'''
import argparse
import os
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-input_folder', metavar='N',help='folder containing all the pbs scripts')
    parser.add_argument('-experiment_name', metavar='N',help='folder containing results for an experiment')
    
    args = parser.parse_args()
    
    count=0
    
    for root, dirs, files in os.walk(os.path.join(args.input_folder)):
        for dir in dirs:
            directory=os.path.join(root,dir,args.experiment_name)
            if os.path.exists(directory):
              shutil.rmtree(directory)
              count+=1
    print "Deleted ",count, "files"