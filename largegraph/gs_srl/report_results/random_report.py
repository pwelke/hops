'''
Created on Jun 29, 2015

@author: irma
'''
'''
Created on Jun 29, 2015

@author: irma
'''
'''
Created on Jun 29, 2015

@author: irma
'''
import argparse,pickle,os,sys,time
import networkx as nx
from sampling_core import sampler_general_ex as smplr
from report_results import report_random_sampling_approach as report
from report_results import make_selected_results_csv as csv_report
import approaches.globals_sampling

def my_version_report(fdict_exhaustive, data_graph, pattern, monitoring_marks, output_path, detailed_result_path, monitoring_reports, exhaustive_approach_results_path, Plist,nr,pattern_file_name,write):
    nr_non_observed_combinations=None
    if write==True:
        size_fdict=len(fdict_exhaustive)
        num_embeddings=0
        for k in fdict_exhaustive.keys():
            num_embeddings = num_embeddings + fdict_exhaustive[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
        nr_possible_combinations=smplr.complete_combinations_1(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
        nr_non_observed_combinations=nr_possible_combinations-size_fdict
        approaches.globals_sampling.nr_non_observed_combinations=nr_non_observed_combinations
    start_time = time.time()
    report.report_monitoring_my_version(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,nr,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations,write)    #print monitoring_reports    


def main(pattern_path,output_folder,result,data,redo,write,monitoring_reports):
    output_path=os.path.join(result,output_folder)
    common_result_path=result
    detailed_result_path=os.path.join(output_path,"monitoring")
    exhaustive_approach_results_path=os.path.join(common_result_path,"exhaustive_results")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=120:
        row=csv_report.get_row(result, output_path, "random",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"random_row.info"),'w') as f:
            f.write(str(row))
        sys.exit()
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    pattern=nx.read_gml(pattern_path)
    fdict_exhaustive=None
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
         pattern_file_name=common_result_path.split("/")[-2]
    
    if  os.path.exists(os.path.join(output_path,'monitoring_reports.pickle')):
        pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
        monitoring_reports=pickle.load(pkl_file)  
    
    if write==True:
        picklename = os.path.join(exhaustive_approach_results_path,"fudict.pickle")
        pickin = open(picklename, 'rb')
        fdict_exhaustive = pickle.load(pickin)
    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)
    approaches.globals_sampling.output_path=output_path
    if pattern_file_name.startswith("dblp"):
       approaches.globals_sampling.experiment_name= "dblp"
    else:
       approaches.globals_sampling.experiment_name= "yeast"
    my_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name,write)    #print monitoring_reports
    row=csv_report.get_row(pattern_path,result, output_path, "random",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,"random_row.info"),'w') as f:
            f.write(str(row))
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-result',help='path to results for a pattern')
    parser.add_argument('-data',help='path to data graph')
    parser.add_argument('-redo',default=False,action='store_true',help='redo report')
    parser.add_argument('-exp',default="my",help='redo report')
    
    
    args = parser.parse_args()
    main(args.result,args.data,args.redo,args.exp,True,None)