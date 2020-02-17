'''
Created on Jun 1, 2017

@author: irma
'''
'''
Created on Aug 4, 2015

@author: irma
'''
import argparse,os
import create_csv_batch_file
import filter_batch_results
import generate_commands_for_reporting
import networkx as nx
import get_patterns_info,csv
import graph_manipulator.graph_analyzer as man
import make_excel_files_results as excel
from decimal import Decimal, ROUND_HALF_UP
from decimal import getcontext

plotall=False
random=False
furer=False
false_furer=False
exhaustive=False
false_furer_order=False


def get_stat(monitoring_directory,experiment_name):
    embeddings=None
    time=None
  
    #read # embeddings
    if os.path.exists(os.path.join(monitoring_directory,'nr_emb.res')):
        with open(os.path.join(monitoring_directory,'nr_emb.res'),'r') as f:
            first_line = f.readline()
            embeddings=float(first_line)
        
    
    #read time
    if os.path.exists(os.path.join(monitoring_directory,'time.res')):
        with open(os.path.join(monitoring_directory,'time.res'),'r') as f:
            first_line = f.readline()
            time=float(first_line)
    
    return (embeddings,time)

def extract_nr_embeddings(path_to_exhaustive_result):
    nr_emb=None
    time=None
    with open(path_to_exhaustive_result,'r') as f:
        for line in f.readlines():
            if line.startswith("Number of embeddings"):
                nr_emb=int(line.split(" ")[3])
            if line.startswith("Exhaustive procedure took"):
                time=int(line.split(" ")[3])
            if line.startswith("Total number of observations:"):
                nr_obs=int(line.split(" ")[4])
    return float(nr_emb),time,int(nr_obs)


def getOBDecomp(path_to_file):
    with open(path_to_file, 'r') as f:
      for line in f.readlines():
            if not(line.startswith("OBDecomp:")) and not(line==""):
                return str(line.rstrip().rstrip().replace("\n",""))

def extract_nr_embeddings_NS(path_to_non_selected):
    nr_emb=None
    time=None
    with open(path_to_non_selected,'r') as f:
        for line in f.readlines():
            if line.startswith("Estimated nr embeddings:"):
                line=line.rstrip().lstrip().replace("\n","")
                nr_emb=round(float(line.split(" ")[3]),3)

    return nr_emb
       
def get_parent_id(pattern_path):
    patt_name=pattern_path.rstrip().split("/")[-1]
    if patt_name=="":
      patt_name=pattern_path.rstrip().split("/")[-2]
    if os.path.exists(os.path.join(pattern_path,patt_name+".parent")):
        with open(os.path.join(pattern_path,patt_name+".parent")) as f:
              for line in f.readlines():
                  return line.rstrip()         
           
def get_row(general_path,pattern_result,experiment_name,pattern_path):
    row={}
    pattern=nx.read_gml(os.path.join(general_path,'input_pattern.gml'))
    parent_id=get_parent_id(os.path.join(pattern_path))
    nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
    cycles=man.is_there_cycle_in_graph(pattern)
    max_degree=man.get_maximum_node_degree(pattern)
    average_degree=man.get_average_node_degree(pattern)
    n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
    #get nr embeddings of exhaustive
    nr_emb=None
    sel_emb=None
    has_obd=True
    emb_stds=[]
    
    if os.path.exists(os.path.join(pattern_result,'no_obdecomp.info')):
        has_obd=False

    if os.path.exists(os.path.join(os.path.dirname(pattern_result),"selected.info")):
        sel_emb=extract_nr_embeddings_NS(os.path.join(os.path.dirname(pattern_result),"selected.info"))
    print "General path: ",general_path
    print os.path.join(general_path,'exhaustive_approach','results_'+general_path.split('/')[-1]+'.res'),"exists?",os.path.exists(os.path.join(general_path,'exhaustive_approach','results_'+general_path.split('/')[-1]+'.res'))
    pattern_name=None
    print general_path.split('/')
    if general_path.split('/')[-1]=="":
        pattern_name=general_path.split('/')[-2]
    else:
        pattern_name=general_path.split('/')[-1]
    print pattern_name
    
    if os.path.exists(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res')):
        nr_emb,time_exh,nr_obs=extract_nr_embeddings(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res'))
    #get the results
    if os.path.exists(pattern_result):
       embeddings,time=get_stat(pattern_result,experiment_name)
    
    clause=None
    if os.path.exists(os.path.join(pattern_path,'clause.info')):
        with open(os.path.join(pattern_path,'clause.info')) as f:
            clause = f.read()

    print "EMBEDDINGS: ",embeddings
    unequal_size_warning=False
    OBD=None
    if os.path.exists(os.path.join(general_path,'results_furer','OBDDecomp.info')):
        OBD=getOBDecomp(os.path.join(general_path,'results_furer','OBDDecomp.info'))
    

    nodes,edges=man.get_readable_text_format(pattern)
    print "PATTERN NAME: ",pattern_result
    
    row['pattern_name']=pattern_result
    row['parent_id']=parent_id
    row['nr_randvar_values']=int(nr_randvar_values)
    row['nodes']=nodes
    row['edges']=edges
    row['has_cycles']=cycles
    row['density']=float(nx.density(pattern))
    row['shape']=man.get_graph_shape(pattern)
    row['max_degree']=float(max_degree)
    row['avg_deg']=float(average_degree)
    row['nr_targets']=n_target_nodes
    row['clause']=clause
    if sel_emb:
      row['sel_emb']=float(sel_emb)
    else:
      row['sel_emb']=sel_emb
    if nr_emb:
      row['exh_emb']=float(nr_emb)
    else:
      row['exh_emb']=nr_emb
    row['has_obd']=has_obd
    #row['unequal_size_warn']=unequal_size_warning
    row['OBD']=OBD
    
    row["emb"]=embeddings
    row["time"]=time
    return row




'''
Returns two writers: for selected CSV and for not selected CSV
'''
def make_csv_writer_sampling_approaches(output_csv_selected,output_csv_not_selected):
    b = open(output_csv_selected, 'w')
    #b1 = open(output_csv_not_selected, 'w')
    field_names=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','sel_emb','exh_emb','OBD','has_obd','emb','time','clause']  
    writer = csv.DictWriter(b, dialect='excel',fieldnames=field_names)
    #writer1 = csv.DictWriter(b1, fieldnames=field_names1)
    writer.writeheader()
    #writer1.writeheader()
    return (writer)




    
def FACT_generate_csvs_known_selected(list_paths_selected_patterns,csv_results,level,generate,pattern_path):
    writer_FACT=make_csv_writer_sampling_approaches(os.path.join(csv_results,"fact_"+level+".csv"),os.path.join(csv_results,"fact_NS_"+level+".csv"))
    counter_selected=0

    for path_selected_pattern in list_paths_selected_patterns:
                print "PATTERN: ",path_selected_pattern
                if plotall==False:
                       print "PATTERN: ",counter_selected
                       counter_selected+=1  
                       row_furer=None
                       print "PATTERN PATH",path_selected_pattern
                       pattern_path_det=os.path.join(pattern_path,path_selected_pattern.split("/")[-2],path_selected_pattern.split("/")[-1])
                       print "Pattern path det: ",pattern_path_det
                       print "Generating the row sdm"
                       row_sdm=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"sdm"),"sdm",pattern_path_det)
                       with open(os.path.join(path_selected_pattern,"sdm","sdm_row.info"),'w') as f:
                           f.write(str(row_sdm))
                           writer_FACT.writerow(row_sdm)

                else:
                       counter_selected+=1  
                       row_sdm=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"sdm"),"sdm",pattern_path_det)                 
                       writer_FACT.writerow(row_sdm)

    print "Number of selected patterns:",counter_selected


  
def make_selected_pattern_file(results,output_file_path,no_batches):
    print "Making selected pattern file ..."
    selected_files=[]
    print "DIR: ",results
    with open(output_file_path,'w') as f:
          for dir in os.listdir(results):
            print "PATH TO RESULT",os.path.join(results,dir)
            if not(no_batches) and not dir.startswith("batch"):
                continue
            else:
               if no_batches:
                   if os.path.exists(os.path.join(results,dir,'selected.info')):
                            f.write(os.path.join(results,dir)+"\n")
                            selected_files.append(os.path.join(results,dir))
               else:
                   for pattern_res in os.listdir(os.path.join(results,dir)):
                        print pattern_res
                        if not os.path.isdir(os.path.join(results,dir,pattern_res)):
                           continue
                        if os.path.exists(os.path.join(results,dir,pattern_res,'selected.info')):
                                f.write(os.path.join(results,dir,pattern_res)+"\n")
                                selected_files.append(os.path.join(results,dir,pattern_res))
    print "FInished creating file: ",output_file_path," with ",len(selected_files),"patterns"
    return selected_files

def make_selected_pattern_file_excep(results,output_file_path,no_batches):
    print "Making selected pattern file EXCEPTION..."
    selected_files=[]
    print "DIR: ",results
    with open(output_file_path,'w') as f:
          for dir in os.listdir(results):
            print "PATH TO RESULT",os.path.join(results,dir)
            if not(no_batches) and not dir.startswith("batch"):
                continue
            else:
                   for pattern_res in os.listdir(os.path.join(results,dir)):
                        print pattern_res
                        if not os.path.isdir(os.path.join(results,dir,pattern_res)):
                           continue
                        
                        f.write(os.path.join(results,dir,pattern_res)+"\n")
                        selected_files.append(os.path.join(results,dir,pattern_res))
    print "FInished creating file: ",output_file_path," with ",len(selected_files),"patterns"
    return selected_files
    
def extract_selected_paths(file):
    print "Extracting selected patterns from ",file
    selected_patterns=[]
    with open(file,'r') as f:
        lines = f.readlines()
        for line in lines:
            selected_patterns.append(line.rstrip().lstrip())
    print "Finished extracting. Found ",len(selected_patterns),"patterns"
    return selected_patterns


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get statistics')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-patterns',help='this is a general path to patterns')
    parser.add_argument('-data',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-plotall',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-generate',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-no_batches',default=False,action='store_true',help='process all the folders in the current path (no batch structure)')
    parser.add_argument('-redo',default=False,action='store_true',help='ignore the fact that selected pattern file was made')
    parser.add_argument('-e',default=False,action='store_true',help='exception: regard all patterns in the result folder to be selected')
    parser.add_argument('-s',default=False,action='store_true',help='generate selected patterns file')


    args = parser.parse_args() 
    results=args.results
    pattern_path=args.patterns
    level=results.split("/")[-2].split("_")[-1]
    selected_patterns=[]
    all=True
    

    plotall=args.plotall
    print "Plotting all?",plotall
    csv_results=os.path.join(os.path.dirname(os.path.dirname(results)),'csv_results')
    if not os.path.exists(csv_results):
        os.makedirs(csv_results)
    
    selected_files=None
    #if list of selected patterns path doesn't exist, make one
    if args.e:
        selected_files=make_selected_pattern_file_excep(results,os.path.join(results,"selected_patterns_list.info"),args.no_batches)

    elif args.generate and args.s:
        selected_files=make_selected_pattern_file(results,os.path.join(results,"selected_patterns_list.info"),args.no_batches)
    elif args.redo and not os.path.exists(os.path.join(results,"selected_patterns_list.info")):
       selected_files=make_selected_pattern_file(results,os.path.join(results,"selected_patterns_list.info"),args.no_batches)
    else:
       selected_files=extract_selected_paths(os.path.join(results,"selected_patterns_list.info"))
    FACT_generate_csvs_known_selected(selected_files,csv_results,level,args.generate,pattern_path)
    print "Written in: ",os.path.join(csv_results)
