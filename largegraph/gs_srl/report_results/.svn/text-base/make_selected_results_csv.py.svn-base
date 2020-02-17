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

def parse_file(file_path,experiment_name):
    getcontext().prec = 11
    nr_iterations=-1
    avg_emb=-1
    nr_iterations=None
    avg_emb=None
    kld=None
    std=None
    with open(file_path,'r') as file:
        for line in file.readlines():
            if line.startswith("number of sampling iterations"):
                strings=line.split(":")
                nr_iterations=int(strings[-1].replace(":","").rstrip().lstrip())
            if line.startswith("average of embeddings")  : 
                strings=line.split(":")
                try:
                   avg_emb=Decimal(strings[-1].replace(":","").rstrip().lstrip())
                   avg_emb=Decimal(avg_emb.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
                except:
                   continue
            if line.startswith("Number of embeddings:")  : 
                strings=line.split(":")
                try:
                   avg_emb=Decimal(strings[-1].replace(":","").rstrip().lstrip()) 
                   avg_emb=Decimal(avg_emb.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
                except:
                   continue
            if line.startswith("stdeviation of"):
                strings=line.split(":")
                std=float(strings[-1].replace(":","").rstrip().lstrip())
            if line.startswith("average average KLD") or line.startswith("average KLD"): 
                strings=line.split("KLD")
                if experiment_name=="furer":
                   kld=float(strings[-1].split(" ")[3].replace(":","").rstrip().lstrip())
                if experiment_name=="false_furer" or experiment_name=="false_furer_order":
                   print experiment_name,"HEY: ",strings,strings[-1],strings,strings[-1].split(" ")[4].replace(":","").rstrip().lstrip()
                   kld=float(strings[-1].split(" ")[4].replace(":","").rstrip().lstrip()) 
                   print "KLD found: ",kld
                   #if kld==None:
                   #   kld=float(strings[-1].split(" ")[4].replace(":","").rstrip().lstrip()) 
                if experiment_name=="random":
                   kld=float(strings[-1].split(" ")[3].replace(":","").rstrip().lstrip()) 
    return (nr_iterations,avg_emb,std,kld)

def get_stat(monitoring_directory,experiment_name):
    embeddings=[] 
    klds=[] 
    emb_stds=[]
    dirs=[]
    for f in os.listdir(monitoring_directory):
        if f.endswith("~") or f.startswith("."):
            continue
        dirs.append(f)
    print "NR files: ",len(dirs)
    for file in sorted(dirs,key = lambda x: int(x.split(".")[0].split("_")[2])):
        if file.endswith("~") or file.startswith("."):
            continue
        print "File: ",os.path.join(monitoring_directory,file)
        nr_iterations,avg_emb,std,kld=parse_file(os.path.join(monitoring_directory,file),experiment_name)
        print nr_iterations,avg_emb,std,kld
        if kld:
          klds.append(float(kld))
        else:
          klds.append(kld)
        if std!=None:
           emb_stds.append(float(std))
        else:
           emb_stds.append(std)
        if avg_emb!=None: 
           embeddings.append(float(avg_emb))
        else:
           embeddings.append(avg_emb)  
    return (embeddings,emb_stds,klds)

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
       
def load_row(file):
    s = open(file, 'r').read()
    s=s.replace("nan","-1")
    row = eval(s)      
    return row 
           
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
        nr_emb,time,nr_obs=extract_nr_embeddings(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res'))
    #get the results
    if os.path.exists(os.path.join(pattern_result,'monitoring')):
       embeddings,emb_stds,klds=get_stat(os.path.join(pattern_result,'monitoring'),experiment_name)
    else:
       embeddings = [None]*120
       klds = [None]*120
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
    
    print "Nr embeddingS: ",len(embeddings)
    for i in xrange(0,len(embeddings)):
        row["emb_"+str(i+1)]=embeddings[i]
        
    for i in xrange(0,len(emb_stds)):
        row["std_"+str(i+1)]=emb_stds[i]
    
    for i in xrange(0,len(klds)):
        row["KLD_"+str(i+1)]=klds[i]
   
    return row

#Get row for non selected patterns!
def get_row_NS(general_path,pattern_result,experiment_name):
    row={}
    if not(os.path.exists(os.path.join(general_path,'input_pattern.gml'))):
        row['pattern_name']=pattern_result
        row['nr_randvar_values']="NC"
        row['nodes']="NC"
        row['edges']="NC"
        row['has_cycles']="NC"
        row['density']="NC"
        row['shape']="NC"
        row['max_degree']="NC"
        row['avg_deg']="NC"
        row['nr_targets']="NC"
        row['nr_emb']="NC"
        row['has_obd']="NC"
        row['unequal_size_warn']="NC"
        row['OBD']="NC"
        return row
        
    pattern=nx.read_gml(os.path.join(general_path,'input_pattern.gml'))
    nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
    cycles=man.is_there_cycle_in_graph(pattern)
    max_degree=man.get_maximum_node_degree(pattern)
    average_degree=man.get_average_node_degree(pattern)
    n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
    nr_emb=None
    has_obd=True
    
    if os.path.exists(os.path.join(pattern_result,'no_obdecomp.info')):
        has_obd=False
    
    if os.path.exists(os.path.join(general_path,'not_selected.info')):
        nr_emb=extract_nr_embeddings_NS(os.path.join(general_path,'not_selected.info'))
    nodes,edges=man.get_readable_text_format(pattern)
    
    unequal_size_warning=False
    if os.path.exists(os.path.join(general_path,'results_furer','unequal_size.warning')):
        unequal_size_warning=True
    OBD=None
    if os.path.exists(os.path.join(general_path,'results_furer','OBDDecomp.info')):
        OBD=getOBDecomp(os.path.join(general_path,'results_furer','OBDDecomp.info')) 
    row['pattern_name']=pattern_result
    row['nr_randvar_values']=nr_randvar_values
    row['nodes']=nodes
    row['edges']=edges
    row['has_cycles']=cycles
    row['density']=nx.density(pattern)
    row['shape']=man.get_graph_shape(pattern)
    row['max_degree']=max_degree
    row['avg_deg']=average_degree
    row['nr_targets']=n_target_nodes
    row['nr_emb']=nr_emb
    #row['has_obd']=has_obd
    #row['unequal_size_warn']=unequal_size_warning
    row['OBD']=OBD
    return row
    

def get_row_exhaustive(general_path,pattern_result,pattern_path):
    row={}
    print "Pattern exhaustive ",pattern_result
    print "Pattern path: ",pattern_path
    pattern=nx.read_gml(os.path.join(general_path,'input_pattern.gml'))
    nr_randvar_values=man.count_nr_randvars_in_graph(pattern)
    cycles=man.is_there_cycle_in_graph(pattern)
    max_degree=man.get_maximum_node_degree(pattern)
    average_degree=man.get_average_node_degree(pattern)
    n_target_nodes=man.get_nr_target_nodes_other_than_head(pattern)
    parent_id=get_parent_id(os.path.join(pattern_path))
    #get nr embeddings of exhaustive
    nr_emb=None
    time=None
    print general_path.split('/')
    pattern_name=general_path.split('/')[-1]
    if pattern_name=="":
        pattern_name=general_path.split('/')[-2]
    nr_obs=None
    print "Exists? ",os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res'),os.path.exists(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res'))
    if os.path.exists(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res')):
        nr_emb,time,nr_obs=extract_nr_embeddings(os.path.join(general_path,'exhaustive_approach','results_'+pattern_name+'.res'))
    
    #get the results
    if os.path.exists(os.path.join(pattern_result,'monitoring')):
       embeddings,stdev,klds=get_stat(os.path.join(pattern_result,'monitoring'),'exhaustive')
    else:
       embeddings = [None]*120
       klds = [None]*120
       
    is_timeout=False   
    if os.path.exists(os.path.join(general_path,'exhaustive_approach','timeout.info')):
           is_timeout=True   
    print "Nr of records for embeddings: ",len(embeddings)
    nodes,edges=man.get_readable_text_format(pattern)
    row['pattern_name']=pattern_result
    row['parent_id']=parent_id
    row['nr_randvar_values']=int(nr_randvar_values)
    row['nodes']=nodes
    row['edges']=edges
    row['has_cycles']=cycles
    row['density']=nx.density(pattern)
    row['max_degree']=float(max_degree)
    row['avg_deg']=float(average_degree)
    row['nr_targets']=int(n_target_nodes)
    if nr_emb:
      row['exh_emb']=float(nr_emb)
    else:
      row['exh_emb']=nr_emb
    row['time']=time
    row['timeout']=is_timeout
    row['nr_observations']=nr_obs
    for i in xrange(1,len(embeddings)+1):
        if embeddings[i-1]==None:
            row["emb_"+str(i)]=None
        else:        
            row["emb_"+str(i)]=float(embeddings[i-1])
    return row


def make_csv_exhaustive(general_results_path,experiment_result_directory_name,output_csv,experiment_name):
    counter_selected=0
    global plotall
    b = open(output_csv, 'w')
    field_names=['pattern_name','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','exh_emb','time','timeout']
    for i in xrange(1,121):
       field_names.append("emb_"+str(i))
    writer = csv.DictWriter(b, fieldnames=field_names)
    writer.writeheader()
    for dir in os.listdir(general_results_path):
        if not dir.startswith("batch"):
            continue
        else:
           for pattern_res in os.listdir(os.path.join(general_results_path,dir)):
               
               if plotall==False:
                   if not os.path.exists(os.path.join(general_results_path,dir,pattern_res,'selected.info')):
                      continue
                   if not os.path.exists(os.path.join(general_results_path,dir,pattern_res,"exhaustive_approach")):
                      continue
               counter_selected+=1  
               row=get_row_exhaustive(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,experiment_result_directory_name))    
               writer.writerow(row)
    print "Number of selected patterns:",counter_selected

'''
Returns two writers: for selected CSV and for not selected CSV
'''
def make_csv_writer_sampling_approaches(output_csv_selected,output_csv_not_selected):
    b = open(output_csv_selected, 'w')
    #b1 = open(output_csv_not_selected, 'w')
    field_names=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','sel_emb','exh_emb','OBD','has_obd']
    #field_names1=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','nr_emb','OBD']
    for i in xrange(1,121):
       field_names.append("emb_"+str(i))
    for i in xrange(1,121):
       field_names.append("std_"+str(i))
    for i in xrange(1,121):
       field_names.append("KLD_"+str(i))    
    writer = csv.DictWriter(b, dialect='excel',fieldnames=field_names)
    #writer1 = csv.DictWriter(b1, fieldnames=field_names1)
    writer.writeheader()
    #writer1.writeheader()
    return (writer)

def make_csv_writer_exhaustive(output_csv):
    b = open(output_csv, 'w')
    field_names=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','exh_emb','time','timeout','nr_observations']
    for i in xrange(1,121):
       field_names.append("emb_"+str(i))
    writer = csv.DictWriter(b, dialect='excel',fieldnames=field_names)
    writer.writeheader()
    return writer


def generate_csvs(general_results_path,csv_results,level):
    #get writer for exhaustive
    writer_exhaustive=make_csv_writer_exhaustive(os.path.join(csv_results,"exhaustive_"+level+".csv"))
    
    #get writer for furer
    writer_furerSEL,writerfurerNS=make_csv_writer_sampling_approaches(os.path.join(csv_results,"furer_"+level+".csv"),os.path.join(csv_results,"furer_NS_"+level+".csv"))
    
    #get writer for false furer
    writer_false_furerSEL,writer_false_furerNS=make_csv_writer_sampling_approaches(os.path.join(csv_results,"Ffurer_"+level+".csv"),os.path.join(csv_results,"Ffurer_NS_"+level+".csv"))
    
     #get writer for false furer
    writer_false_furerSEL_order,writer_false_furerNS_order=make_csv_writer_sampling_approaches(os.path.join(csv_results,"Ffurer_order_random_"+level+".csv"),os.path.join(csv_results,"Ffurer_NS_order_random_"+level+".csv"))
    
    
    #get writer for false random
    writer_randomSEL,writer_randomNS=make_csv_writer_sampling_approaches(os.path.join(csv_results,"random"+level+".csv"),os.path.join(csv_results,"random_NS_"+level+".csv"))
    counter_selected=0
    
    for dir in os.listdir(general_results_path):
        if not dir.startswith("batch"):
            continue
        else:
           for pattern_res in os.listdir(os.path.join(general_results_path,dir)):
                if not os.path.isdir(os.path.join(results,dir,pattern_res)):
                   continue
                if plotall==False:
                    if os.path.exists(os.path.join(general_results_path,dir,pattern_res,'selected.info')):
                       print "PATTERN: ",counter_selected
                       counter_selected+=1  
                       row_furer=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_furer"),"furer")
                       row_Ffurer=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_false_furer"),"false_furer")
                       row_Ffurer_order=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_false_furer_order_random"),"false_furer_order")

                       row_random=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"random_vertex_approach"),"random")
                       writer_furerSEL.writerow(row_furer)
                       writer_false_furerSEL_order.writerow(row_Ffurer_order)
                       writer_false_furerSEL.writerow(row_Ffurer)
                       writer_randomSEL.writerow(row_random)     
                       row_exhaustive=get_row_exhaustive(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"exhaustive_approach"))  
                       writer_exhaustive.writerow(row_exhaustive) 
                else:
                       counter_selected+=1  
                       row_furer=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_furer"),"furer")
                       row_Ffurer=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_false_furer"),"false_furer")
                       row_random=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"random_vertex_approach"),"random")
                       row_Ffurer_order=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,"results_false_furer_order_random"),"false_furer_order")
                       writer_false_furerSEL_order.writerow(row_Ffurer_order)
                       writer_furerSEL.writerow(row_furer)
                       writer_false_furerSEL.writerow(row_Ffurer)
                       writer_randomSEL.writerow(row_random)  
    print "Number of selected patterns:",counter_selected
    
def generate_csvs_known_selected(list_paths_selected_patterns,csv_results,level,generate,pattern_path):
    global furer
    global random
    global false_furer
    global false_furer_order
    global exhaustive
    #get writer for exhaustive
    if exhaustive:
      writer_exhaustive=make_csv_writer_exhaustive(os.path.join(csv_results,"exhaustive_"+level+".csv"))
    
    #get writer for furer
    if furer:
       writer_furerSEL=make_csv_writer_sampling_approaches(os.path.join(csv_results,"furer_"+level+".csv"),os.path.join(csv_results,"furer_NS_"+level+".csv"))
    
    #get writer for false furer
    if false_furer:
       writer_false_furerSEL=make_csv_writer_sampling_approaches(os.path.join(csv_results,"Ffurer_"+level+".csv"),os.path.join(csv_results,"Ffurer_NS_"+level+".csv"))
       
    if false_furer_order:
       writer_false_furerSEL_order=make_csv_writer_sampling_approaches(os.path.join(csv_results,"Ffurer_order_random_"+level+".csv"),os.path.join(csv_results,"Ffurer_NS_order_random_"+level+".csv"))
    
    #get writer for false random
    if random:
       writer_randomSEL=make_csv_writer_sampling_approaches(os.path.join(csv_results,"random_"+level+".csv"),os.path.join(csv_results,"random_NS_"+level+".csv"))
    counter_selected=0

    for path_selected_pattern in list_paths_selected_patterns:
                print "PATTERN: ",path_selected_pattern
                if plotall==False:
                       print "PATTERN: ",counter_selected
                       counter_selected+=1  
                       row_furer=None
                       print "PATH: ",os.path.join(path_selected_pattern,"results_furer","furer_row.info")
                       print "PATTERN PATH",path_selected_pattern
                       pattern_path_det=os.path.join(pattern_path,path_selected_pattern.split("/")[-2],path_selected_pattern.split("/")[-1])
                       
                       
                       if furer and os.path.exists(os.path.join(path_selected_pattern,"results_furer")):
                           if not generate and os.path.exists(os.path.join(path_selected_pattern,"results_furer","furer_row.info")):
                               print "Loading the row Furer"
                               row_furer=load_row(os.path.join(path_selected_pattern.rstrip().lstrip(),"results_furer","furer_row.info"))
                           else:
                               print "Generating the row Furer"
                               row_furer=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_furer"),"furer",pattern_path_det)
                               with open(os.path.join(path_selected_pattern,"results_furer","furer_row.info"),'w') as f:
                                   f.write(str(row_furer))
                           writer_furerSEL.writerow(row_furer)
                       else:
                           print "Not marking results of Furer"
                       
                       if false_furer and os.path.exists(os.path.join(path_selected_pattern,"results_false_furer")):
                           if not generate and os.path.exists(os.path.join(path_selected_pattern,"results_false_furer","false_furer_row.info")):
                               print "Loading the row False Furer"
                               row_Ffurer=load_row(os.path.join(path_selected_pattern.rstrip().lstrip(),"results_false_furer","false_furer_row.info"))
                           else:
                               print "Generating the row False Furer"
                               row_Ffurer=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_false_furer"),"false_furer",pattern_path_det)
                               with open(os.path.join(path_selected_pattern,"results_false_furer","false_furer_row.info"),'w') as f:
                                   f.write(str(row_Ffurer))
                           writer_false_furerSEL.writerow(row_Ffurer)
                       else:
                           print "Not marking resluts of False furer"
                           
                       if false_furer_order and os.path.exists(os.path.join(path_selected_pattern,"results_false_furer_order_random")):
                           if not generate and os.path.exists(os.path.join(path_selected_pattern,"results_false_furer_order_random","false_furer_row_order_random.info")):
                               print "Loading the row False Furer"
                               row_Ffurer=load_row(os.path.join(path_selected_pattern.rstrip().lstrip(),"results_false_furer_order_random","false_furer_row_order_random.info"))
                           else:
                               print "Generating the row False Furer"
                               row_Ffurer=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_false_furer_order_random"),"false_furer_order",pattern_path_det)
                               with open(os.path.join(path_selected_pattern,"results_false_furer_order_random","false_furer_row_order_random.info"),'w') as f:
                                   f.write(str(row_Ffurer))
                           writer_false_furerSEL_order.writerow(row_Ffurer)
                       else:
                           print "Not marking resluts of False furer order"
                       
                       if random and os.path.exists(os.path.join(path_selected_pattern,"random_vertex_approach")):
                          if not generate and os.path.exists(os.path.join(path_selected_pattern,"random_vertex_approach","random_row.info")):
                               print "Loading the row for Random"
                               row_random=load_row(os.path.join(path_selected_pattern.rstrip().lstrip(),"random_vertex_approach","random_row.info"))
                          else:
                               print "Generating the row for Random"
                               row_random=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"random_vertex_approach"),"random",pattern_path_det)
                               with open(os.path.join(path_selected_pattern,"random_vertex_approach","random_row.info"),'w') as f:
                                   f.write(str(row_random))
                          writer_randomSEL.writerow(row_random) 
                       
                       if exhaustive and os.path.exists(os.path.join(path_selected_pattern,"exhaustive_approach")):
                           if not generate and os.path.exists(os.path.join(path_selected_pattern,"exhaustive_approach","exhaustive_info_row.info")):
                              print "Loading the row Exhaustive"
                              row_exhaustive=load_row(os.path.join(path_selected_pattern.rstrip().lstrip(),"exhaustive_approach","exhaustive_info_row.info")) 
                           else:
                              print "Generating the row Exhaustive"
                              row_exhaustive=get_row_exhaustive(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"exhaustive_approach"),pattern_path_det)  
                           writer_exhaustive.writerow(row_exhaustive)
                       else:
                           print "Not marking reslults of exhaustive" 
                else:
                       counter_selected+=1  
                       row_furer=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_furer"),"furer",pattern_path_det)
                       row_Ffurer=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_false_furer"),"false_furer",pattern_path_det)
                       row_Ffurer_order=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"results_false_furer_order"),"false_furer_order",pattern_path_det)
                       row_random=get_row(os.path.join(path_selected_pattern),os.path.join(path_selected_pattern,"random_vertex_approach"),"random",pattern_path_det)
                       writer_furerSEL.writerow(row_furer)
                       writer_false_furerSEL.writerow(row_Ffurer)
                       writer_false_furerSEL_order.writerow(row_Ffurer_order)
                       writer_randomSEL.writerow(row_random)  
    print "Number of selected patterns:",counter_selected


def make_csv(general_results_path,experiment_result_directory_name,output_csv_selected,output_csv_not_selected,experiment_name):
    global plotall
    counter_selected=0
    b = open(output_csv_selected, 'w')
    b1 = open(output_csv_not_selected, 'w')
    field_names=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','sel_emb','exh_emb','OBD','has_obd']
    field_names1=['pattern_name','parent_id','nr_randvar_values','nodes','edges','nr_targets','shape','has_cycles','density','max_degree','avg_deg','nr_emb','OBD']

    for i in xrange(1,121):
       field_names.append("emb_"+str(i))
    for i in xrange(1,121):
       field_names.append("KLD_"+str(i))    
       
    writer = csv.DictWriter(b, fieldnames=field_names)
    writer1 = csv.DictWriter(b1, fieldnames=field_names1)
    writer.writeheader()
    writer1.writeheader()
    for dir in os.listdir(general_results_path):
        if not dir.startswith("batch"):
            continue
        else:
           for pattern_res in os.listdir(os.path.join(general_results_path,dir)):
                if not os.path.isdir(os.path.join(results,dir,pattern_res)):
                   continue
                if plotall==False:
                    if not os.path.exists(os.path.join(general_results_path,dir,pattern_res,'selected.info')):
                       row1=get_row_NS(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,experiment_result_directory_name),experiment_name)
                       writer1.writerow(row1)
                    else:
                       counter_selected+=1  
                       row=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,experiment_result_directory_name),experiment_name)
                       writer.writerow(row)
                else:
                       counter_selected+=1  
                       row=get_row(os.path.join(results,dir,pattern_res),os.path.join(results,dir,pattern_res,experiment_result_directory_name),experiment_name)
                       writer.writerow(row)
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
    global plotall
    global all
    global random
    global furer
    global false_furer
    global false_furer_order
    global exhaustive
    parser = argparse.ArgumentParser(description='get statistics')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-patterns',help='this is a general path to patterns')
    parser.add_argument('-data',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-plotall',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-generate',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-random',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-furer',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-false_furer',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-exhaustive',default=False,action='store_true',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
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
    
    if(args.random or args.furer or args.false_furer or args.exhaustive):
        all=False
     
    random=args.random
    exhaustive=args.exhaustive
    furer=args.furer
    false_furer=args.false_furer
    
    if all:
        random=True
        exhaustive=True
        furer=True
        false_furer=True
        false_furer_order=True
    
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
    generate_csvs_known_selected(selected_files,csv_results,level,args.generate,pattern_path)
    print "Written in: ",os.path.join(csv_results)
    excel.create_workbook(csv_results,level)
    print "Created workbook!"