'''
Created on Jul 8, 2015

@author: irma
'''
import os
from experiments import sampler_general_ex as smplr
from experiments import sampling_utils as su
import numpy,pickle
import networkx as nx

def getStatistics_furer(fudicts,fdict_exhaustive,pattern,data_graph,target_indices,targe_ids,head_node,target_nodes,detailed_result_path,pattern_file_name):
    #CREATE DIRECTORY THAT WILL CONTAIN RESULTS FOR EACH TIME INSTANCE     
    furer_results_KLD = []
    furer_results_bhatta = []
    furer_results_hellinger = []
    furer_times = []
    observed_nodes=[]
    observed_nodes_difference_per_snapshot=[]
          
    snapshot_directory_path=os.path.join(detailed_result_path)
    if not(os.path.exists(snapshot_directory_path)):
        os.mkdir(snapshot_directory_path)
    snapshot_directory_file=os.path.join(snapshot_directory_path,'statistics.info')
    
    #filter out exhaustive dictionary
    filtered_f_dict_exhaustive={}
    for key in fdict_exhaustive.keys():
        new_key=()
        for target in target_indices:
            new_key+=(key[target-1])
        if not new_key in filtered_f_dict_exhaustive.keys():    
            filtered_f_dict_exhaustive[new_key]=0
        if new_key in filtered_f_dict_exhaustive.keys():
            filtered_f_dict_exhaustive[new_key]+=fdict_exhaustive[key]
            
    #filter out furer dictionaries
    filtered_fudicts=[]
    fudict_monitors=fudicts[0]
    for dict in fudict_monitors:
        temp_fudict={}
        for key in dict.keys():
           new_key=()
           for target in target_indices:
               new_key+=(key[target-1])
           if not new_key in temp_fudict.keys():    
               temp_fudict[new_key]=0
           if new_key in temp_fudict.keys():
               temp_fudict[new_key]+=dict[key]
        filtered_fudicts.append(temp_fudict)
        
    smplr.complete_combinations(filtered_f_dict_exhaustive, data_graph,  pattern,  targe_ids)      # add zeros to all not present combinations
    smplr.smooth(filtered_f_dict_exhaustive,  filtered_f_dict_exhaustive)
    
    fdict_limited = filtered_fudicts[1]
    smplr.smooth(fdict_limited,filtered_f_dict_exhaustive)
    fdict_Furer=filtered_fudicts[1]
    [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default(filtered_f_dict_exhaustive,  trash_factor=0.01)
    [pdl,  tl,  dk] = smplr.make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
    [pdf ,  tl,  dk]= smplr.make_pd_general_kickout_default_limited(fdict_Furer,  trash_list,  default_key)
    
    furer_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
    furer_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
    furer_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))    



def get_target_nodes(pattern,Plist):
   target_nodes_as_in_tupple=[]
   for node in Plist:
       if pattern.node[node]['target']==True:
           target_nodes_as_in_tupple.append(node)
   return target_nodes_as_in_tupple
           

if __name__ == '__main__':
    picklename = os.path.join('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/RESULTS/test_pattern_5/exhaustive_approach',"fdict_exhaustive_test_pattern_5.pickle")
    pickin = open(picklename, 'rb')
    fdict_exhaustive = pickle.load(pickin)
    
    picklename = os.path.join('/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/RESULTS/test_pattern_5/results_furer',"fudicts.pickle")
    pickin = open(picklename, 'rb')
    fudicts = pickle.load(pickin)
    
    pkl_file = open(os.path.join("/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/RESULTS/test_pattern_5/results_furer",'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    
    pattern=nx.read_gml("/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/PATTERNS/test_pattern_5/test.gml")
    head_node=pattern.node[2]
    target_nodes=[pattern.node[4]]
    
    target_nodes_as_in_tupple=get_target_nodes(pattern,Plist)
    print target_nodes_as_in_tupple
    print Plist
    data_graph=nx.read_gpickle("/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/RESULTS/Yeast/big_pattern/YEAST.gpickle")
    
    detailed_result_path="/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/RESULTS/test_pattern_5/results_furer/dep1/"
    
    pattern_file_name="test"
    getStatistics_furer(fudicts,fdict_exhaustive,pattern,data_graph,[1,2],[5,2],head_node,target_nodes,detailed_result_path,pattern_file_name)
  
#       print "Writing to: ",snapshot_directory_file
#       resultfile = open(snapshot_directory_file,  'w')
#       resultfile.write('Furer\n')
#       resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
#       resultfile.write(" " +"\n")
#       resultfile.write("average average KLD on furer: " + str(numpy.mean(furer_results_KLD))  + " with SSTD: " + str(numpy.std(furer_results_KLD,  ddof=1)) +"\n")
#       resultfile.write("average average bhatta on furer: " + str(numpy.mean(furer_results_bhatta))  + " with SSTD: " + str(numpy.std(furer_results_bhatta,  ddof=1)) +"\n")
#       resultfile.write("average average hellinger on furer: " + str(numpy.mean(furer_results_hellinger))  + " with SSTD: " + str(numpy.std(furer_results_hellinger,  ddof=1)) +"\n")
#       resultfile.write(" " +"\n")
#       resultfile.write('-----DETAILED RESULTS-----' +"\n")
#       resultfile.write('furer_results_KLD : ' + str(furer_results_KLD) +"\n")
#       resultfile.write('furer_results_bhatta : ' + str(furer_results_bhatta) +"\n")
#       resultfile.write('furer_results_hellinger : ' + str(furer_results_hellinger) +"\n")
#       resultfile.write('avg #nodes observed : ' + str(numpy.mean(observed_nodes)) +"\n")
#       resultfile.write("------------------------------------ Sampling info ------------------------------\n")
#       resultfile.write('number of sampling iterations : ' + str(nr_iterations[counter])+"\n")    
#       resultfile.write('average of embeddings : ' + str(sum_of_embeddings[counter]/nr_iterations[counter])+"\n")        
#       #resultfile.write('average of embeddings w.r.t sampling iterations:' + str(sum_of_embeddings[counter]/float(nr_iterations[counter]))+"\n") 
#       a=sum_of_squares[counter]-((math.pow(sum_of_embeddings[counter], 2)/nr_iterations[counter]))
#       #a=(nr_iterations[counter]*sum_of_squares[counter])-(math.pow(sum_of_embeddings[counter], 2))
#       stdeviation=math.sqrt(a/(nr_iterations[counter]-1))
#       resultfile.write('stdeviation of # embeddings: ' + str(stdeviation)+"\n") 
#       resultfile.close()
#       counter+=1
#      counter_duration+=1 