'''
Created on Oct 27, 2016

@author: irma
'''
import argparse,os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-r', help='this is a general path to results for patterns(containing results for all patterns sizes')
    parser.add_argument('-s1',default=4,type=int,help='initial pattern size')
    parser.add_argument('-s2',default=10,type=int,help='end pattern size')

    args = parser.parse_args() 
    
    nr_selected=0
    nr_timedout_exhaustive=0
    
    for i in xrange(args.s1,args.s2+1):
        path=args.r+"/patterns_size_"+str(i)
        #list batches
        for batch in os.listdir(path):
            if batch.startswith("batch"):
                #go through all the pattens
                print "P1:",os.path.join(path,batch)
                for pat in os.listdir(os.path.join(path,batch)):
                    print "oattern : ",pat
                    print "P2:",os.path.join(path,batch,pat,'selected.info')
                    if os.path.exists(os.path.join(path,batch,pat,'selected.info')):
                        nr_selected+=1
                    if os.path.exists(os.path.join(path,batch,pat,'exhaustive_approach','timeout.info')):
                        nr_timedout_exhaustive+=1
    
    print "nr selected: ",nr_selected
    print "nr timeout exhaustive",nr_timedout_exhaustive
    print "percentage: ",(float(nr_timedout_exhaustive)/float(nr_selected))*100