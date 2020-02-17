'''
Created on May 5, 2015

@author: irma
'''
import argparse
import os
import shutil
import pickle
import networkx as nx
import graph_manipulator.graph_analyzer as man
import csv
import re
import numpy
 
 
def graph_characteristics_csv(pattern_path, output_path):
     csv_folder_summary=os.path.join(output_path,'graph_characteristics_csv')
     if not os.path.exists(csv_folder_summary):
        os.makedirs(csv_folder_summary)
     batch_number=pattern_path.split("/")[-1] 
     file=csv_folder_summary+"/"+batch_number+'_results_final_limit.csv'
     print "Making file: ",file
     b = open(file, 'w')
     field_names=['pattern_name','nr_randvar_values','nr_targets','has_cycles','max_degree','average_degree']
     writer = csv.DictWriter(b, fieldnames=field_names)
     writer.writeheader()
     pattern_file_gml=None
     print "Number of patterns: ",len(sorted(os.listdir(pattern_path),key = lambda x: x[:-5]))
     
     for patt in sorted(os.listdir(pattern_path),key = lambda x: x[:-5]):
        print os.path.join(pattern_path,patt)
        if(os.path.isfile(os.path.join(pattern_path,patt))):
           continue
        pattern_file_gml=os.path.join(pattern_path,patt,patt+".gml")
        #if patt.endswith(".gml"):
        #    pattern_file_gml=os.path.join(pattern_path,patt)
        print "Pattern file gml",pattern_file_gml
        if pattern_file_gml!=None:
            pattern=nx.read_gml(pattern_file_gml)
        else:
            continue
        pattern_file_name=patt
        #some general pattern charactersitics
        nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
        cycles=man.is_there_cycle_in_graph(pattern)
        max_degree=man.get_maximum_node_degree(pattern)
        average_degree=man.get_average_node_degree(pattern)
        n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
        row={}
        row['pattern_name']=pattern_file_name
        row['nr_randvar_values']=str(nr_randvar_values)
        row['nr_targets']=str(n_target_nodes)
        row['has_cycles']=str(cycles)
        row['max_degree']=str(max_degree)
        row['average_degree']=str(average_degree)
        writer.writerow(row)
     print "Finished writing csv ...to",file
     return file
    
def makecsv_file_for_final_limits(pattern_path,output_path,redo):
    print "Output path: ",output_path
    print "Pattern path: ",pattern_path
    csv_folder_summary=os.path.join(output_path,'csv_results')
    batch_number=pattern_path.split("/")[-1]
    print batch_number
    print "Does exist csv folder summary",csv_folder_summary,os.path.exists(csv_folder_summary)
    if not os.path.exists(csv_folder_summary):
        os.makedirs(csv_folder_summary)
    file=csv_folder_summary+"/"+batch_number+'_results_final_limit.csv'
    if os.path.exists(file) and redo==False:
        print "Results for this batch already exist"
        return
    b = open(file, 'w')

    field_names=['pattern_name','selected','nr_randvar_values','nr_targets','has_cycles','exh_emb','rnd_emb','furer_emb','ffurer_emb','limit16_rnd_emb','limit16_fur_emb','limit16_ff_emb','rnd_KLD_16','furer_KLD_16','ff_KLD_16','exh_rt','rnd_avgRT_16','furer_avgRT_16','ff_avgRT_16']
    writer = csv.DictWriter(b, fieldnames=field_names)
    writer.writeheader()
    print "Number of patterns: ",len(sorted(os.listdir(pattern_path),key = lambda x: x[:-5]))
    
    counter=1
    nr_patterns=len(os.listdir(pattern_path))
    for patt in sorted(os.listdir(pattern_path),key = lambda x: x[:-5]):
        print "CSV processing :",nr_patterns," th pattern"
        nr_patterns-=1
        if(os.path.isfile(os.path.join(pattern_path,patt))):
           continue
        pattern_file_gml=None
        print "Path",os.path.join(pattern_path,patt)
        if os.path.exists(os.path.join(pattern_path,patt,"results_furer","input_pattern.gml")):
            pattern_file_gml=os.path.join(pattern_path,patt,"results_furer","input_pattern.gml")
        elif os.path.exists(os.path.join(pattern_path,patt,'exhaustive_approach','input_pattern.gml')):
            pattern_file_gml=os.path.join(pattern_path,patt,'exhaustive_approach','input_pattern.gml')
        elif patt.endswith(".gml"):
            pattern_file_gml=os.path.join(pattern_path,patt)
        print "Pattern file gml",pattern_file_gml
        if pattern_file_gml!=None:
            pattern=nx.read_gml(pattern_file_gml)
        else:
            continue    
        pattern_file_name=patt
        #PICKLES RESULTS PATH
        exhaustive_file_result=os.path.join(pattern_path,patt,'exhaustive_approach','results_'+str(pattern_file_name)+".res")
        random_dict_result=os.path.join(pattern_path,patt,'random_vertex_approach','rndicts.pickle')
        furer_dict_result=os.path.join(pattern_path,patt,'results_furer','fudicts.pickle')
        false_furer_dict_result=os.path.join(pattern_path,patt,'results_false_furer','fudicts.pickle')
        
        #NLIMITS RESULTS PATH
        random_nlimits_result=os.path.join(pattern_path,patt,'random_vertex_approach','n_limits')
        furer_nlimits_result=os.path.join(pattern_path,patt,'results_furer','n_limits')
        false_furer_nlimits_result=os.path.join(pattern_path,patt,'results_false_furer','n_limits')
        
        #some general pattern charactersitics
        nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
        cycles=man.is_there_cycle_in_graph(pattern)
        max_degree=man.get_maximum_node_degree(pattern)
        average_degree=man.get_average_node_degree(pattern)
        n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
        
        nr_embeddings_exhaustive,exhaustive_running_time=extract_number_of_embeddings_and_rt_exhaustive(exhaustive_file_result)
        nr_embeddings_random_final_limit=[]
        nr_embeddings_furer_final_limit=[]
        nr_embeddings_false_furer_final_limit=[]
        nr_embeddings_furer_final=-1
        nr_embeddings_false_furer_final=-1
        nr_embeddings_random_final=-1
        furer_klds=[]
        furer_SSTDs=[]
        false_furer_kld=[]
        false_furer_SSTDs=[]
        random_klds=[]
        random_SSTDs=[]
        furer_avg_rt=[]
        false_furer_avg_rt=[]
        random_avg_rt=[]
        
        #FIRST CHECK IF EXPPERIMENTS WERE RUN IN SEQUENTIALL OR PARALLEL MODE. IF IT'S PARALLEL MODE RESULTS HAVE TO BE
        #EXTRACTED FROM RUN DIRECTORIES
        #EXTRACT RANDOM VERTEX RESULTS
        if os.path.exists(os.path.join(pattern_path,patt,'random_vertex_approach')): 
            files_random = sorted([f for f in os.listdir(os.path.join(pattern_path,patt,'random_vertex_approach')) if re.match('run_*', f)])        
            if(len(files_random)!=0):
                random_klds,random_SSTDs,random_avg_rt=extract_KLD_sampling_approach_parallel_run(os.path.join(pattern_path,patt,'random_vertex_approach'),files_random) 
                nr_embeddings_random_final=extract_final_number_of_embeddings_sampling_approach(os.path.join(pattern_path,patt,'random_vertex_approach'))
            else:
                random_klds,random_SSTDs,random_avg_rt=extract_KLD_sampling_approach(random_nlimits_result)
                #nr_embeddings_random_final_limit=extract_number_of_embeddings_sampling_approach(random_dict_result)
                nr_embeddings_random_final=extract_final_number_of_embeddings_sampling_approach(os.path.join(pattern_path,patt,'random_vertex_approach'))
            
        #EXTRACT FURER RESULTS
        if os.path.exists(os.path.join(pattern_path,patt,'results_furer')):
            print "FURER" 
            files_furer = sorted([f for f in os.listdir(os.path.join(pattern_path,patt,'results_furer')) if re.match('run_*', f)])   
            if(len(files_furer)!=0):
                furer_klds,furer_SSTDs,furer_avg_rt=extract_KLD_sampling_approach_parallel_run(os.path.join(pattern_path,patt,'results_furer'),files_furer) 
                nr_embeddings_furer_final=extract_final_number_of_embeddings_sampling_approach(os.path.join(pattern_path,patt,'results_furer'))
            else:
                furer_klds,furer_SSTDs,furer_avg_rt=extract_KLD_sampling_approach(furer_nlimits_result)
                #nr_embeddings_furer_final_limit=extract_number_of_embeddings_sampling_approach(furer_dict_result)
                nr_embeddings_furer_final=extract_final_number_of_embeddings_sampling_approach(os.path.join(pattern_path,patt,'results_furer'))

            
        #EXTRACT FALSE FURER TIMES
        if os.path.exists(os.path.join(pattern_path,patt,'results_false_furer')): 
            files_false_furer = sorted([f for f in os.listdir(os.path.join(pattern_path,patt,'results_false_furer')) if re.match('run_*', f)])
            if(len(files_false_furer)!=0):
                false_furer_kld,false_furer_SSTDs,false_furer_avg_rt=extract_KLD_sampling_approach_parallel_run(os.path.join(pattern_path,patt,'results_furer'),files_false_furer) 
                nr_embeddings_false_furer_final_limit=extract_number_of_embeddings_sampling_approach(random_dict_result) 
            else:
                false_furer_kld,false_furer_SSTDs,false_furer_avg_rt=extract_KLD_sampling_approach(false_furer_nlimits_result)
                #nr_embeddings_false_furer_final_limit=extract_number_of_embeddings_sampling_approach(false_furer_dict_result)
                nr_embeddings_false_furer_final=extract_final_number_of_embeddings_sampling_approach(os.path.join(pattern_path,patt,'results_false_furer'))

        print "PATH ",os.path.join(pattern_path,patt,'selected.info'),os.path.exists(os.path.join(pattern_path,patt,'selected.info'))
        selected=False
        #check if pattern selected
        if os.path.exists(os.path.join(pattern_path,patt,'selected.info')):
            selected=True
                 
        row={}
        row['pattern_name']=pattern_file_name
        row['selected']=selected
        row['nr_randvar_values']=str(nr_randvar_values)
        row['nr_targets']=str(n_target_nodes)
        row['has_cycles']=str(cycles)
                  
        if(nr_embeddings_exhaustive=='NC'):
            row['exh_emb']='NC'
        else:
            row['exh_emb']=nr_embeddings_exhaustive
        row['rnd_emb']=nr_embeddings_random_final
        row['furer_emb']=nr_embeddings_furer_final
        row['ffurer_emb']=nr_embeddings_false_furer_final
        row['limit16_rnd_emb']="None"
        row['limit16_fur_emb']="None"
        row['limit16_ff_emb']="None"
        row['rnd_KLD_16']=str(str(getNTH_limit_value(15,random_klds))+" +- "+str(getNTH_limit_value(15,random_SSTDs)))
        row['furer_KLD_16']=str(str(getNTH_limit_value(15,furer_klds))+" +- "+str(getNTH_limit_value(15,furer_SSTDs)))
        row['ff_KLD_16']=str(str(getNTH_limit_value(15,false_furer_kld))+" +- "+str(getNTH_limit_value(15,false_furer_SSTDs)))
        row['exh_rt']=exhaustive_running_time
        row['rnd_avgRT_16']=getNTH_limit_value(15,random_avg_rt)
        row['furer_avgRT_16']=getNTH_limit_value(15,furer_avg_rt)
        row['ff_avgRT_16']=getNTH_limit_value(15,false_furer_avg_rt) 
        writer.writerow(row)
        counter+=1
        #return path tocreated csv file
    print "Finished writing csv ...to",file
    return file

        
        

def getNTH_limit_value(N,array_nlimit_results):
    if len(array_nlimit_results)<=N:
        return 'NC'
    if len(array_nlimit_results)==0:
        return 'NR'
    else:
        return array_nlimit_results[N]
    
        

               
def extract_number_of_embeddings_and_rt_exhaustive(path_to_exhaustive_file):
    #this means that no embeddings was found for this pattern
    if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(path_to_exhaustive_file)),'no_results.info')):
          print "No embeddings found for exhaustive approach "
          return []
    
    if not os.path.exists(path_to_exhaustive_file):
        return 'NC'
           
    with open(path_to_exhaustive_file,'r') as f:
        for line in f.readlines():
            if line.startswith('Number of embeddings:'):
                split_line=line.split(':')
                nr_embeddings=int(split_line[-1].lstrip().replace("\n",""))
            if line.startswith('Exhaustive procedure took'):
                time=float(line.split(" ")[3])
    return nr_embeddings,time
        


def extract_number_of_embeddings_sampling_approach_parallel_runs(path_to_results,run_file_directories,pickle_name):
    nlimit_embeddings={}
    result_embeddings=[]
    for f in run_file_directories:
      pickle_file=os.path.join(path_to_results,f,pickle_name)
      nr_embeddings=extract_number_of_embeddings_sampling_approach(pickle_file)

      for n in nr_embeddings.keys():
          if not n in nlimit_embeddings.keys():
              nlimit_embeddings[n]=[]
          nlimit_embeddings[n].append(nr_embeddings[n])
          
    for n in nr_embeddings.keys():
          nlimit_embeddings[n]=numpy.average(nlimit_embeddings[n])
          result_embeddings.append(nlimit_embeddings[n])

    return result_embeddings
      
    

'''
Give a pickled file containing frequencies, extract number of embeddings
for each observation limit
'''        
def extract_number_of_embeddings_sampling_approach(file_to_pickled_dictionary):
    if not os.path.exists(file_to_pickled_dictionary):
        return []
    #print "loading pickle..."
    pkl_file = open(file_to_pickled_dictionary, 'rb')
    repetitions=pickle.load(pkl_file)  
    #print "pickle loaded"
    number_of_embeddings=0
    nlimit_embeddings_for_runs={}
    nr_runs=len(repetitions) 
    #collect all the embeddings - for each nlimit into one dictionary
    #keys correspond to the limit (1 for the first, second second)
    #the number of observations with each limit can be found in nlimit folder
    for run in repetitions:
       counter=1
       for nlimit in run:
           if counter not in nlimit_embeddings_for_runs.keys():
               nlimit_embeddings_for_runs[counter]=0
           if(len(nlimit)==1):
               #means there were no heads, targets, whatever
               if '()' in nlimit.keys():    
                  nlimit_embeddings_for_runs[counter]=nlimit_embeddings_for_runs[counter]+int(nlimit[()])   
               else:
                  nlimit_embeddings_for_runs[counter]=nlimit_embeddings_for_runs[counter]+len(nlimit)                
           else:
               for key in nlimit.keys():
                   nlimit_embeddings_for_runs[counter]+=nlimit[key]
           counter+=1
    
    #average the counts of embeddings for each limit over the number of runs
    for k in nlimit_embeddings_for_runs.keys():
        nlimit_embeddings_for_runs[k]=int(nlimit_embeddings_for_runs[k]/float(nr_runs))  
    return nlimit_embeddings_for_runs

'''
Give a pickled file containing frequencies, extract number of embeddings
for each observation limit
'''        
def extract_final_number_of_embeddings_sampling_approach(path_to_results):
    if not os.path.exists(os.path.join(path_to_results,"final_embeddings.info")):
        return []
    else:
        #print os.path.join(path_to_results,"final_embeddings.info")
        with open(os.path.join(path_to_results,"final_embeddings.info"),"r") as f:
            for line in f.readlines():
                return float(line.rstrip())


'''
Given a path to nlimits for an approach, go through all nlimits (in ascending
order) and collect average KLDs over 10 runs
'''
def extract_KLD_sampling_approach_parallel_run(path_to_approach,files):
    nlimit_KLDs_for_runs={}
    avgRTs=[]
    KLDs=[]
    SSTDs=[]
    nlimits=[]
    file_base=None
    nr_repetitions=None  
    #EXTRACT NLIMITS
    path_to_nlimits=os.path.join(path_to_approach,"n_limits")
    if not os.path.exists(path_to_nlimits):
            print "doesn't exist n_limits result"
            return [],[],[]      
    elif os.path.exists(path_to_nlimits) and len(os.listdir(path_to_nlimits))==0:
            print "doesn't exist n_limits result"
            return [],[],[] 
    
    for f in files:
      print os.path.join(path_to_approach,"n_limits")
      for nlimit in os.listdir(os.path.join(path_to_approach,"n_limits")):
        if not nlimit.endswith('.result'):
            continue             
        split_on_periosd=str(nlimit).split(".")
        #print split_on_periosd
        file_base=split_on_periosd[0]
        #take the second to last part
        nlimit_var=split_on_periosd[-2]
        nlimits.append(int(nlimit_var.split('x')[1]))
        if nr_repetitions==None:
            nr_repetitions=int(nlimit_var.split('x')[0])    
           #sort the limits
        sorted_nlimits=sorted(nlimits)
      break   
   
    nlimits_to_kld_runs={}
    nlimits_to_sstd_runs={}
    nlimits_to_avgRT_runs={}
        
    for n in sorted_nlimits:
        nlimits_to_kld_runs[n]=[]
        nlimits_to_sstd_runs[n]=[]
        nlimits_to_avgRT_runs[n]=[]
    
    for file in files:
        path_to_nlimits=os.path.join(path_to_approach,"n_limits")   
        if not os.path.exists(path_to_nlimits):
            print "doesn't exist n_limits result"
            return [],[],[]      
        elif os.path.exists(path_to_nlimits) and len(os.listdir(path_to_nlimits))==0:
            print "doesn't exist n_limits result"
            return [],[],[] 
        for n in sorted_nlimits:
            file=file_base+"."+str(nr_repetitions)+'x'+str(n)+".result"
            #load file
            with open(os.path.join(path_to_nlimits,file)) as f:
             # print os.path.join(path_to_nlimits,file)     
              for line in f.readlines(): 
                if line.startswith('average average KLD'):
                    info=line.split(":")    
                    KLD=round(float(info[1].split(" ")[1]),3)
                    SSTD=round(float(info[2]),3)
                    nlimits_to_kld_runs[n].append(KLD)
                    nlimits_to_sstd_runs[n].append(SSTD)
                
                if line.startswith('randnode_times'):
                    info=line.split(":") 
                    string_array=info[1].replace("]","").replace("[","").split(",")
                    times=0
                    for s in string_array:
                        times+=round(float(s),2)
                    nlimits_to_avgRT_runs[n].append(times)
                    
                if line.startswith('false_times'):
                    info=line.split(":") 
                    string_array=info[1].replace("]","").replace("[","").split(",")
                    times=0
                    for s in string_array:
                        times+=round(float(s),2)
                    nlimits_to_avgRT_runs[n].append(times)
                    
                if line.startswith('furer_times'):
                    info=line.split(":") 
                    string_array=info[1].replace("]","").replace("[","").split(",")
                    times=0
                    for s in string_array:
                        times+=round(float(s),2)
                    nlimits_to_avgRT_runs[n].append(times)
    
    #CALCULATE AVERAGE OF THE VALUES
    for n in sorted_nlimits:
        KLD_value=numpy.average(nlimits_to_kld_runs[n])
        SSTD_value=numpy.std(nlimits_to_kld_runs[n])
        avgRTs_value=numpy.average(nlimits_to_avgRT_runs[n])
        KLDs.append(round(KLD_value,2))
        SSTDs.append(round(SSTD_value,2))
        avgRTs.append(round(avgRTs_value,2))
        
    return KLDs,SSTDs,avgRTs




'''
Given a path to nlimits for an approach, go through all nlimits (in ascending
order) and collect average KLDs over 10 runs
'''
def extract_KLD_sampling_approach(path_to_nlimits):
    nlimit_KLDs_for_runs={}
   
    avgRTs=[]
    KLDs=[]
    SSTDs=[]
    nlimits=[]
    
    file_base=None
    nr_repetitions=None
    
    if not os.path.exists(path_to_nlimits):
        return [],[],[]
    
    for file in os.listdir(path_to_nlimits):
        
        if not file.endswith('.result'):
            continue
        
        split_on_periosd=str(file).split(".")
        if file_base==None:
            file_base=split_on_periosd[0]
        #take the second to last part
        nlimit=split_on_periosd[-2]
        
        
        nlimits.append(int(nlimit.split('x')[1]))
        if nr_repetitions==None:
            nr_repetitions=int(nlimit.split('x')[0])
    
    #sort the limits
    sorted_nlimits=sorted(nlimits)
    
    for n in sorted_nlimits:
        file=file_base+"."+str(nr_repetitions)+'x'+str(n)+".result"
        #load file
        with open(os.path.join(path_to_nlimits,file)) as f:
          for line in f.readlines():
            
            if line.startswith('average average KLD'):
                info=line.split(":")    
                KLD=round(float(info[1].split(" ")[1]),3)
                SSTD=round(float(info[2]),3)
                KLDs.append(KLD)
                SSTDs.append(SSTD)
            
            if line.startswith('randnode_times'):
                info=line.split(":") 
                string_array=info[1].replace("]","").replace("[","").split(",")
                times=0
                for s in string_array:
                    times+=round(float(s),2)
                avgRTs.append(times/nr_repetitions)
                
            if line.startswith('false_times'):
                info=line.split(":") 
                string_array=info[1].replace("]","").replace("[","").split(",")
                times=0
                for s in string_array:
                    times+=round(float(s),2)
                avgRTs.append(times/nr_repetitions) 
                
            if line.startswith('furer_times'):
                info=line.split(":") 
                string_array=info[1].replace("]","").replace("[","").split(",")
                times=0
                for s in string_array:
                    times+=round(float(s),2)
                avgRTs.append(times/nr_repetitions) 
    
    return KLDs,SSTDs,avgRTs



def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-path_to_results', metavar='N',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-path_to_report', metavar='N',help='this is a general path to completed results')
    args = parser.parse_args()
    #Make CSV for final limits:
    makecsv_file_for_final_limits(args.path_to_results,args.path_to_report,True)
