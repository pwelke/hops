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
from experiments import sampler_general_ex as smplr
import report_false_furer as report
import make_selected_results_csv as csv_report
import experiments.globals

def my_version_report(fdict_exhaustive, data_graph, pattern, monitoring_marks, output_path, detailed_result_path, monitoring_reports, exhaustive_approach_results_path, Plist,nr,pattern_file_name,write):
    experiments.globals.report="furer"
    nr_non_observed_combinations=None
    start_time = time.time()
    if write==True:
        size_fdict=len(fdict_exhaustive)
        num_embeddings=0
        for k in fdict_exhaustive.keys():
            num_embeddings = num_embeddings + fdict_exhaustive[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
        print  "NR EMBEDDINGS BEFORE COMPLETING: ",num_embeddings
        
        nr_possible_combinations=smplr.complete_combinations_1(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
        nr_non_observed_combinations=nr_possible_combinations-size_fdict
    experiments.globals.nr_non_observed_combinations=nr_non_observed_combinations
    report.report_monitoring_my_version(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,nr,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations,write)    #print monitoring_reports    
    print "ELAPSED TIME: ",time.time() - start_time
    
def martin_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,nr,pattern_file_name):
    print "LEN FDICT_EXHAUSTIVE (BEFORE): ",len(fdict_exhaustive)
    size_fdict=len(fdict_exhaustive)
    num_embeddings=0
    for k in fdict_exhaustive.keys():
        num_embeddings = num_embeddings + fdict_exhaustive[k]
    start_time = time.time()
    nr_possible_combinations=smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
    smplr.smooth(fdict_exhaustive,  fdict_exhaustive)
    report.report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,nr,pattern_file_name,fdict_exhaustive)    #print monitoring_reports    
    print "ELAPSED TIME: ",time.time() - start_time

def main(result,data,redo,write,monitoring_reports):
    flag_version='my'
    common_result_path=result
    output_path=os.path.join(result,'results_false_furer')
    exhaustive_approach_results_path=os.path.join(common_result_path,"exhaustive_approach")
    detailed_result_path=os.path.join(output_path,"monitoring")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=120:
        print "Results already post-processed"
        row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"false_furer_row.info"),'w') as f:
            f.write(str(row))
        sys.exit()
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    #data_graph=nx.read_gpickle(data)
    pattern=nx.read_gml(os.path.join(common_result_path,'input_pattern.gml'))
    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    #load monitoring_reports
    pattern_file_name=common_result_path.split("/")[-1]    
    fdict_exhaustive=None
    if pattern_file_name=="":
        pattern_file_name=common_result_path.split("/")[-2]
        
    if os.path.exists(os.path.join(output_path,'monitoring_reports.pickle')):
        pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
        monitoring_reports=pickle.load(pkl_file)  
        
    if write==True:
        picklename = os.path.join(exhaustive_approach_results_path,"fdict_exhaustive_%s.pickle" %pattern_file_name)
        pickin = open(picklename, 'rb')
        fdict_exhaustive = pickle.load(pickin)
    
    
    
    print common_result_path.split("/")
    
        
    
    experiments.globals.output_path=output_path
    if pattern_file_name.startswith("dblp"):
       experiments.globals.experiment_name="dblp"
    else:
       experiments.globals.experiment_name="yeast"
    #smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
    #smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
    #Report the results
    print "Monitoring report..."
    if(flag_version=='my'):
        my_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name,write)    #print monitoring_reports    
    if(flag_version=='martin'):
        martin_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name)    #print monitoring_reports    

    #report.report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,1,pattern_file_name)    #print monitoring_reports    
    row=csv_report.get_row(result, output_path, "false_furer",result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,"false_furer_row.info"),'w') as f:
            f.write(str(row))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-result',help='path to results for a pattern')
    parser.add_argument('-data',help='path to data graph')
    parser.add_argument('-redo',default=False,action='store_true',help='redo report')
    args = parser.parse_args()
    main(args.result,args.data,args.redo,True,None)
    