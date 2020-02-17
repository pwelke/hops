'''
Created on Jun 29, 2015

@author: irma
'''
'''
Created on Jun 29, 2015

@author: irma
'''
import time
import argparse,pickle,os,sys
import networkx as nx
from sampling_core import sampler_general_ex as smplr
import report_false_furer as report
import make_selected_results_csv as csv_report
import approaches.globals_sampling
import numpy

def my_version_report_online(fdict_exhaustive, data_graph, pattern, monitoring_marks, output_path, detailed_result_path, monitoring_reports, exhaustive_approach_results_path, Plist_base,nr,pattern_file_name):
    approaches.globals_sampling.report= "furer"
    size_fdict=len(fdict_exhaustive)
    num_embeddings=0
    for k in fdict_exhaustive.keys():
        num_embeddings = num_embeddings + fdict_exhaustive[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
    results={}
    counter=1
    for i in monitoring_reports.keys():
       approaches.globals_sampling.nr_non_observed_combinations=0
       nr_possible_combinations=smplr.complete_combinations_1(fdict_exhaustive, data_graph,  pattern,  Plist_base)      # add zeros to all not present combinations
       nr_non_observed_combinations=nr_possible_combinations-size_fdict
       approaches.globals_sampling.nr_non_observed_combinations=nr_non_observed_combinations
       results[counter]=report.report_monitoring_my_version_online(monitoring_marks,output_path,detailed_result_path,monitoring_reports[i],exhaustive_approach_results_path,data_graph,pattern,Plist_base,nr,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations)    #print monitoring_reports    
       counter+=1

    for i in range(len(monitoring_marks)):
        avg_klds=[]
        average_bhattas=[]
        average_hellingers=[]
        std_klds=[]
        std_bhattas=[]
        std_hellingers=[]
        avg_nodes_observed=[]
        nr_nodes_per_time_interval_per_runs=[]
        number_of_sampling_iterations=[]
        average_of_embeddings=[]
        stdevs=[]
        with open(os.path.join(detailed_result_path,'res_time_'+str(monitoring_marks[i])+".info"),'w') as resultfile:
           resultfile.write('False Furer with different orderings\n')
           for k in monitoring_reports.keys():
               #print "run:",k,results[k]['average_klds']
               avg_klds.append(results[k]['average_klds'][i])
               average_bhattas.append(results[k]['average_bhattas'][i])
               average_hellingers.append(results[k]['average_hellingers'][i])
               std_klds.append(results[k]['std_klds'][i])
               std_bhattas.append(results[k]['std_bhattas'][i])
               std_hellingers.append(results[k]['std_hellingers'][i])
               avg_nodes_observed.append(results[k]['avg_nodes_observed'][i])
               nr_nodes_per_time_interval_per_runs.append(results[k]['nr_nodes_per_time_interval_per_runs'][i])
               number_of_sampling_iterations.append(results[k]['number_of_sampling_iterations'][i])
               average_of_embeddings.append(float(results[k]['average_of_embeddings'][i]))
               stdevs.append(results[k]['stdevs'][i])
           resultfile.write("average KLD on false furer: " + str(numpy.mean(avg_klds))  + " with SSTD: " + str(numpy.std(avg_klds,ddof=1)) +"\n")
           resultfile.write("average bhatta on false furer: " + str(numpy.mean(average_bhattas))  + " with SSTD: " + str(numpy.std(average_bhattas,ddof=1)) +"\n")
           resultfile.write("average hellinger on false furer: " + str(numpy.mean(average_hellingers))  + " with SSTD: " + str(numpy.std(average_hellingers,ddof=1)) +"\n")
           resultfile.write(" " +"\n")
           resultfile.write('avg #nodes observed :' + str(numpy.mean(avg_nodes_observed)) +"\n")
           resultfile.write('average of embeddings : ' + str(numpy.mean(average_of_embeddings))+"\n")
           resultfile.write('stdeviation of # embeddings: ' +str(numpy.nanmean(stdevs))+"\n")

def main(result,data,redo,name_of_folder):
    common_result_path=result
    output_path=os.path.join(result,name_of_folder)
    exhaustive_approach_results_path=os.path.join(result,"exhaustive_approach")
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    #data_graph=nx.read_gpickle(data)
    pattern=nx.read_gml(os.path.join(output_path,'input_pattern.gml'))
    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist_base.pickle'), 'rb')
    Plist_base=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    #load monitoring_reports
    pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
    monitoring_reports=pickle.load(pkl_file)  
    
    
    detailed_result_path=os.path.join(output_path,"monitoring")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=120:
        row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,name_of_folder+".info"),'w') as f:
            f.write(str(row))
        sys.exit()
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
        pattern_file_name=common_result_path.split("/")[-2]
        
    picklename = os.path.join(exhaustive_approach_results_path,"fdict_exhaustive_%s.pickle" %pattern_file_name)
    pickin = open(picklename, 'rb')
    fdict_exhaustive = pickle.load(pickin)
    approaches.globals_sampling.output_path=output_path
    if pattern_file_name.startswith("dblp"):
       approaches.globals_sampling.experiment_name= "dblp"
    else:
       approaches.globals_sampling.experiment_name= "yeast"

    my_version_report_online(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist_base,1,pattern_file_name)    #print monitoring_reports
    row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,name_of_folder+".info"),'w') as f:
            f.write(str(row))
            
def main_1(result,data,redo,name_of_folder,monitoring_reports):
    common_result_path=result
    output_path=os.path.join(result,name_of_folder)
    exhaustive_approach_results_path=os.path.join(result,"exhaustive_approach")
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    pattern=nx.read_gml(os.path.join(output_path,'input_pattern.gml'))
    pkl_file = open(os.path.join(output_path,'Plist_base.pickle'), 'rb')
    Plist_base=pickle.load(pkl_file)  
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)
    detailed_result_path=os.path.join(output_path,"monitoring")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=120:
        row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,name_of_folder+".info"),'w') as f:
            f.write(str(row))
        sys.exit()
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
        pattern_file_name=common_result_path.split("/")[-2]
        
    picklename = os.path.join(exhaustive_approach_results_path,"fdict_exhaustive_%s.pickle" %pattern_file_name)
    pickin = open(picklename, 'rb')
    fdict_exhaustive = pickle.load(pickin)
    approaches.globals_sampling.output_path=output_path
    if pattern_file_name.startswith("dblp"):
       approaches.globals_sampling.experiment_name= "dblp"
    else:
       approaches.globals_sampling.experiment_name= "yeast"

    my_version_report_online(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist_base,1,pattern_file_name)    #print monitoring_reports
    row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,name_of_folder+".info"),'w') as f:
            f.write(str(row))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-result',help='path to results for a pattern')
    parser.add_argument('-data',help='path to data graph')
    parser.add_argument('-redo',default=False,action='store_true',help='redo report')
    args = parser.parse_args()
    main(args.result,args.data,args.redo,'results_false_furer_order_random')
    
