'''
Created on Nov 25, 2015

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
    for batch in os.listdir(args.r):
        if "batch" in batch:
            for pattern_result in os.listdir(os.path.join(args.r,batch)):
                path_to_result=os.path.join(args.r,batch,pattern_result)
                pattern_to_be_removed=path_to_result.replace("RESULTS","PATTERNS")
                print os.path.join(path_to_result)
                if len(os.listdir(os.path.join(path_to_result)))==0 or not os.path.exists(os.path.join(path_to_result,"selected.info")):
                #if  len(os.listdir(os.path.join(path_to_result)))==0 and os.path.exists(os.path.join(path_to_result,"not_selected.info")) or os.path.exists(os.path.join(path_to_result,"not_preselected.info")):
                    removing+=1
                    if os.path.exists(pattern_to_be_removed):
                      shutil.rmtree(pattern_to_be_removed)
                    shutil.rmtree(path_to_result)
                else:
                    not_removing+=1
    
