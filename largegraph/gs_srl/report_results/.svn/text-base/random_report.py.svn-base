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
from experiments import sampler_general_ex as smplr
import report_random_sampling_approach as report
import make_selected_results_csv as csv_report
import experiments.globals

def my_version_report(fdict_exhaustive, data_graph, pattern, monitoring_marks, output_path, detailed_result_path, monitoring_reports, exhaustive_approach_results_path, Plist,nr,pattern_file_name,write):
    nr_non_observed_combinations=None
    if write==True:
        print "LEN FDICT_EXHAUSTIVE (BEFORE): ",len(fdict_exhaustive)
        size_fdict=len(fdict_exhaustive)
        num_embeddings=0
        for k in fdict_exhaustive.keys():
            num_embeddings = num_embeddings + fdict_exhaustive[k]  # I remove +1 added by Laplace smoothing BEWARE: previous Laplace smoothing assumed
        nr_possible_combinations=smplr.complete_combinations_1(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
        nr_non_observed_combinations=nr_possible_combinations-size_fdict
        experiments.globals.nr_non_observed_combinations=nr_non_observed_combinations
        print  "NR EMBEDDINGS BEFORE COMPLETING: ",num_embeddings
    #for k in fdict_exhaustive:
    #              print k,fdict_exhaustive[k]
    start_time = time.time()
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
   #smplr.smooth(fdict_exhaustive,  fdict_exhaustive)
    report.report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,nr,pattern_file_name)    #print monitoring_reports    
    print "ELAPSED TIME: ",time.time() - start_time


def main(result,data,redo,exp,write,monitoring_reports):
    print "************************************** Reporting random for ",result,"*************************************************"
    flag_version=exp
    print "Running version: ",flag_version
    output_path=os.path.join(result,'random_vertex_approach')
    common_result_path=result
    detailed_result_path=os.path.join(output_path,"monitoring")
    exhaustive_approach_results_path=os.path.join(common_result_path,"exhaustive_approach")
    if (not redo) and os.path.exists(detailed_result_path) and len(os.listdir(detailed_result_path))>=120:
        print "Results already post-processed"
        row=csv_report.get_row(result, output_path, "random",result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"random_row.info"),'w') as f:
            f.write(str(row))
        sys.exit()
    try:
      data_graph=nx.read_gpickle(data)
    except:
      data_graph=nx.read_gml(data)
    #data_graph=nx.read_gpickle(data)
    pattern=nx.read_gml(os.path.join(common_result_path,'input_pattern.gml'))
    with open(os.path.join(result,'root_node.dec'),'r') as f:
        for line in f.readlines():
            root_node=int(line.split(" ")[0])
            root_node_predicate_name=str(line.split(" ")[1].rstrip().lstrip())
            break
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate']==pattern.node[root_node]['predicate']]
    print "NR root nodeS: ",len(root_nodes)
    experiments.globals.nr_root_nodes=len(root_nodes)
    
    fdict_exhaustive=None
    pattern_file_name=common_result_path.split("/")[-1]
    if pattern_file_name=="":
         pattern_file_name=common_result_path.split("/")[-2]
    
    if  os.path.exists(os.path.join(output_path,'monitoring_reports.pickle')):
        pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
        monitoring_reports=pickle.load(pkl_file)  
    
    if write==True:
        picklename = os.path.join(exhaustive_approach_results_path,"fdict_exhaustive_%s.pickle" %pattern_file_name)
        pickin = open(picklename, 'rb')
        fdict_exhaustive = pickle.load(pickin)
        
        
    print "Nr monitoring reports: ",len(monitoring_reports)
    #load Plist
    pkl_file = open(os.path.join(output_path,'Plist.pickle'), 'rb')
    Plist=pickle.load(pkl_file)  
    #load monitoring marks
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    
    experiments.globals.output_path=output_path
    if pattern_file_name.startswith("dblp"):
       experiments.globals.experiment_name="dblp"
    else:
       experiments.globals.experiment_name="yeast"
       
    if(flag_version=='my'):
        my_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name,write)    #print monitoring_reports    
    if(flag_version=='martin'):
        martin_version_report(fdict_exhaustive,data_graph,pattern,monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,Plist,1,pattern_file_name)    #print monitoring_reports    

    #smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
    #smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
    #Report the results
    #print "Monitoring report..."
    #report.report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_results_path,data_graph,pattern,Plist,1,pattern_file_name)    #print monitoring_reports    
    row=csv_report.get_row(result, output_path, "random",result.replace("RESULTS","PATTERNS"))
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