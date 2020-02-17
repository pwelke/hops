'''
Created on Dec 14, 2016

@author: irma
'''
import argparse,os,shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r',help='path to results for a pattern')
    
    args = parser.parse_args()
    batches=[]
    not_removing=0
    removing=0
    count=0
    for batch in os.listdir(args.r):
        if "batch" in batch:
            for pattern_result in os.listdir(os.path.join(args.r,batch)):
                path_to_result=os.path.join(args.r,batch,pattern_result)
                pattern_to_be_removed=path_to_result.replace("RESULTS","PATTERNS")
                if os.path.exists(os.path.join(path_to_result)):
                    count+=1
    with open(os.path.join(args.r,"patterns_processed.info"),'w') as f:
        f.write(str(count))
        