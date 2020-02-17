'''
Created on Apr 18, 2017

@author: irma
'''
import argparse,os,shutil


def main(result_path,N):
    for dir in os.listdir(result_path):
        if not dir.startswith("batch"):
            continue
        #list patterns in batch
        counter=0
        for p in os.listdir(os.path.join(result_path,dir)):
                    if os.path.exists(os.path.join(result_path,dir,p,'selected.info')):
                            counter+=1
                            if N!=-1 and counter>=N:
                                #remove the selected
                                shutil.rmtree(os.path.join(result_path,dir,p,'selected.info'))
                              
                         

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r',help='path to results')
    parser.add_argument('-N',default=-1,help='promote N files')
    args = parser.parse_args()  
    main(args.r,args.N)