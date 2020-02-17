'''
Created on Nov 25, 2015

@author: irma
'''
import argparse,os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-pattern_path',help='path to results for a pattern')
    parser.add_argument('-level',type=int,help='redo report')
    
    args = parser.parse_args()
    batches=[]
    for batch in os.listdir(args.pattern_path):
        filename=os.path.join(args.pattern_path,batch,"all_patterns_"+str(args.level)+".pickle")
        if not batch.startswith("batch"):
            continue
        else:
            if os.path.isfile(filename):
                batches.append(batch)
    
    counter=1
    for b in batches:
        print b
        if counter==1:
            counter+=1
            continue
        if counter==len(batches):
            counter+=1
            continue
        filename=os.path.join(args.pattern_path,"batch"+str(counter),"all_patterns_"+str(args.level)+".pickle")
        print "removing: ",os.path.join(args.pattern_path,"batch"+str(counter),"all_patterns_"+str(args.level)+".pickle")
        if os.path.isfile(filename):
             os.remove(filename)
        counter+=1
        