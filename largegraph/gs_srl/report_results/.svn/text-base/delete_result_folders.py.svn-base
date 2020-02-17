'''
Created on Nov 25, 2015

@author: irma
'''
import argparse,os,shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r',help='path to results for a pattern')
    parser.add_argument('-f',help='folder name')

    
    args = parser.parse_args()
    batches=[]
    for batch in os.listdir(args.r):
        if not os.path.isdir(os.path.join(args.r,batch)):
            continue
        for patt_result in os.listdir(os.path.join(args.r,batch)):
            path_to_random_res=os.path.join(args.r,batch,patt_result)
            print "Removing: ",os.path.join(path_to_random_res,args.f)
            if os.path.exists(os.path.join(path_to_random_res,args.f)):
               shutil.rmtree(os.path.join(path_to_random_res,args.f))
            #if os.path.exists(os.path.join(path_to_random_res,args.f)):
            #   os.remove(os.path.join(path_to_random_res,args.f))