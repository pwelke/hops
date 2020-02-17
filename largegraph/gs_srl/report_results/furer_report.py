'''
Created on Jun 29, 2015

@author: irma
'''
import time
import argparse,pickle,os,sys
import networkx as nx
from sampling_core import sampler_general_ex as smplr
import report_furer_approach as report
import make_selected_results_csv as csv_report
import approaches.globals_sampling

def my_version_report(fdict_exhaustive, data_graph, pattern, monitoring_marks, output_path, detailed_result_path, monitoring_reports, exhaustive_approach_results_path, Plist,nr,pattern_file_name,write):
    approaches.globals_sampling.report= "furer"
    nr_non_observed_combinations=None
    if write==True:
        size_fdict=len(fdict_exhaustive)
        num_embeddings=0
        for k in fdict_exhaustive.keys():
            num_embeddings = num_embeddings + fdict_exhaustive[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
        nr_possible_combinations=smplr.complete_combinations_1(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
        nr_non_observed_combinations=nr_possible_combinations-size_fdict
        approaches.globals_sampling.nr_non_observed_combinations=nr_non_observed_combinations
    report.report_monitoring_my_version(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,nr,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations,write)    #print monitoring_reports

def main(pattern_path,output_folder,result,data,redo,write,monitoring_reports):
    common_result_path=result
    output_path=os.path.join(result,output_folder)
    detailed_result_path=os.path.join(output_path,"monitoring")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=100:
        row=csv_report.get_row(result, output_path, "furer",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"furer_row.info"),'w') as f:
            f.write(str(row))
        sys.exit()
    exhaustive_approach_results_path=os.path.join(common_result_path,"exhaustive_results")
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    pattern=nx.read_gml(pattern_path)
    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    #load monitoring_reports
    if os.path.exists(os.path.join(output_path,'monitoring_reports.pickle')):
        pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
        monitoring_reports=pickle.load(pkl_file)  
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
        pattern_file_name=common_result_path.split("/")[-2]
    fdict_exhaustive=None
    if os.path.exists(os.path.join(exhaustive_approach_results_path, "fudict.pickle")):
        pickin = open(os.path.join(exhaustive_approach_results_path, "fudict.pickle"))
        fdict_exhaustive = pickle.load(pickin)
    approaches.globals_sampling.output_path=output_path


    my_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name,write)    #print monitoring_reports
    row=csv_report.get_row(pattern_path,result, output_path, "furer",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,"furer_row.info"),'w') as f:
            f.write(str(row))


def main_hops(pattern_path,output_folder,result,data,redo,write,monitoring_reports, data_graph, pattern):
    common_result_path=result
    output_path=os.path.join(result,output_folder)
    detailed_result_path=os.path.join(output_path,"monitoring")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=100:
        row=csv_report.get_row(result, output_path, "furer",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"furer_row.info"),'w') as f:
            f.write(str(row))
        sys.exit()
    exhaustive_approach_results_path=os.path.join(common_result_path,"exhaustive_results")

    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    #load monitoring_reports
    if os.path.exists(os.path.join(output_path,'monitoring_reports.pickle')):
        pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
        monitoring_reports=pickle.load(pkl_file)  
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
        pattern_file_name=common_result_path.split("/")[-2]
    fdict_exhaustive=None
    if os.path.exists(os.path.join(exhaustive_approach_results_path, "fudict.pickle")):
        pickin = open(os.path.join(exhaustive_approach_results_path, "fudict.pickle"))
        fdict_exhaustive = pickle.load(pickin)
    approaches.globals_sampling.output_path=output_path


    my_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name,write)    #print monitoring_reports
    row=csv_report.get_row(pattern_path,result, output_path, "furer",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,"furer_row.info"),'w') as f:
            f.write(str(row))

    

        
if __name__=='__main__':
        parser = argparse.ArgumentParser(description='Run exhaustive approach')
        parser.add_argument('-result',help='path to results for a pattern')
        parser.add_argument('-data',help='path to data graph')
        parser.add_argument('-redo',default=False,action='store_true',help='redo report')
        parser.add_argument('-write',default=False,action='store_true',help='redo report')
        args = parser.parse_args()
        main(args.result,args.data,args.redo,args.write,None)
        