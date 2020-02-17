'''
Created on May 4, 2015

@author: irma
'''
import argparse
import os
import pickle
import patternGenerator.generate_pattern as gen
from report_results import directory_manager
import yeast_network.yeast_experimenter as yeast
import dblp_network.dblp_experimenter as dblp
import networkx.algorithms.isomorphism as iso
import networkx as nx


def main(batch_path,pattern_level,previous_batch,output,data_label,N,png):
    current_batch=previous_batch+1
    #load pickle of previous batch
    print "loading pickle..."
    pickle_name="all_patterns_"+str(pattern_level)+".pickle"
    
    #irma changed this for YEAST problem of memory. We only use pickles from batch1. Usually we would do it sequentially
    batch_path_adapted=batch_path.replace("batch"+str(previous_batch),"batch1")
    print "Loading pickle from: ",batch_path_adapted
    path_to_pickle=os.path.join(batch_path_adapted,pickle_name)
    if not os.path.exists(path_to_pickle):
      print "No pickle for this pattern. Exiting ...."
      return
    pkl_file = open(path_to_pickle, 'rb')
    patterns=pickle.load(pkl_file)
    print "pickle loaded"
    
    #output_path_new_batch=os.path.join(output,"batch"+str(current_batch))
    output_path_new_batch_pickle=os.path.join(output,"batch1")
    output_path_new_batch_patterns=os.path.join(output,"batch"+str(current_batch))

    if(not(os.path.exists(output_path_new_batch_patterns))):
        os.makedirs(output_path_new_batch_patterns)
      
    result,the_rest=gen.randomly_sample_N_non_isomorphic_patterns(patterns,N) 
    
    print "No pickling I changed this"
    print "Need to pickle the rest! Too large to detect isomorphisms"
    
    #write the rest of patterns in the file as a pickle
    print "pickling to: ",output_path_new_batch_pickle+'/all_patterns_'+str(pattern_level)+'.pickle'
    with open(output_path_new_batch_pickle+'/all_patterns_'+str(pattern_level)+'.pickle','w') as f:
     pickle.dump(the_rest,f)

    print "Pickling finished..."
   
    #writing selected patterns to the directory
    print "Outputing to: ",output_path_new_batch_patterns
    directory_manager.write_patterns_in_list(result,data_label, output_path_new_batch_patterns,png)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-batch_path',help='path to patterns of previous batch')
    parser.add_argument('-pattern_level',type=int,help='level of the current batchi-ing')
    parser.add_argument('-batch_number',type=int,help='number of previous batch')
    parser.add_argument('-output',help='output of the new batch (no need to specify "batch" in the parameter')
    parser.add_argument('-data_label',help='data set short label. All pattern names will begin with this name')
    parser.add_argument('-N',type=int,help='data set short label. All pattern names will begin with this name')
    parser.add_argument('-png',default=False,action="store_true",help='data set short label. All pattern names will begin with this name')


    args = parser.parse_args()
    main(args.batch_path,args.pattern_level,args.batch_number,args.output,args.data_label,args.N,args.png)
    
    
    
    
