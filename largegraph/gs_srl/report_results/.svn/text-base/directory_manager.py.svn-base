'''
Created on Mar 10, 2015

@author: irma
'''
import os.path
import networkx as nx
import uuid,time
import graph_manipulator.graph_analyzer as ganal
import patternGenerator.generate_pattern as gen_pat
from graph_manipulator import visualization as vis
'''
Write patterns in the list with a general file label
and in a specific directory.
'''
def write_patterns_in_list(list_of_patterns,file_label,directory,png):
    print "Number of patterns to write: ",len(list_of_patterns)
    print "Output directory: ",directory
    i=0
    for pattern in list_of_patterns:
        #Write pattern in a readable format 
        i+=1
        file_name=file_label+'pattern_'+str(uuid.uuid4().hex)
        dir=os.path.join(directory,file_name)
       
        file_path=os.path.join(dir,file_name+".gml")
        if not os.path.exists(dir):
                os.makedirs(dir)
        else:
            print "DIRECTORY ALREADY EXISTS!! AAAA"
        if pattern_relationship_invalid(pattern):
           with open(os.path.join(dir,'invalid.info'),'w') as f:
                f.write('invalid pattern. Relation node neighbourhood <2.')
        
        for node in pattern.nodes():
            pattern.node[node]['type']=None
            
        ganal.pattern_to_readable_text_format(pattern, dir+"/"+file_name+".readable")    
        nx.write_gml(pattern, file_path)
        print "PARENT PATTERN NAME: ",pattern.name
        parent_file_path=os.path.join(dir,file_name+".parent")
        with open(parent_file_path, 'w') as the_file:
            the_file.write(pattern.name)
        print "********************************************"
        for node in pattern.nodes():
            print pattern.node[node]

        if png==True:
            vis.visualize_graph(pattern,os.path.join(directory,file_name,file_name))
            
    filtered_list,list_for_removal,pairs=gen_pat.find_isomorphic_graphs(list_of_patterns)
    print "isomorphic found: ",len(list_for_removal)
            
def pattern_relationship_invalid(pattern):
    for node in pattern.nodes():
        if(str(pattern.node[node]['type']).rstrip().lstrip()=="relation"):
            if(len(nx.neighbors(pattern, node))<2): #warning: allowed this here!!!
                return True
            if(len(nx.neighbors(pattern, node))>2):
                return True
    return False
           
def load_graphs_in_folder(network_type_specification,folder):
    gml_files_tmp=[]
    result=[]
    graphs=[]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.gml'):
                gml_files_tmp.append(os.path.join(root,file))    
    for file in gml_files_tmp:
        graph=nx.read_gml(file, False)
        graph.name=file
        graphs.append(graph)
    #add types to nodes in graphs!!!
    for graph in graphs:
        new_graph=network_type_specification.turn_gml_graph_to_type_graph(graph)
        result.append(new_graph)
    return result

'''given pattern folder and results folder, extract selected patterns and use them
for further extensions'''
def load_selected_graphs(network_type_specification,pattern_folder,results_folder):
    gml_files_tmp=[]
    parents=[]
    result=[]
    graphs=[]
    print "Pattern folder: ",pattern_folder
    for batch in os.listdir(pattern_folder):
        if not batch.startswith("batch"):
            continue
        else:
            for pattern in os.listdir(os.path.join(pattern_folder,batch)):   
                print os.path.join(results_folder,batch,pattern),os.path.exists(os.path.join(results_folder,batch,pattern,'selected.info'))
                if os.path.exists(os.path.join(results_folder,batch,pattern,'selected.info')):
                    gml_files_tmp.append(os.path.join(pattern_folder,batch,pattern,pattern+".gml"))  
                    parents.append(os.path.join(pattern_folder,batch,pattern,pattern+".parent"))          
    counter=0
    for file in gml_files_tmp:
        graph=nx.read_gml(file)
        graph.name=parents[counter]
        counter+=1
        graphs.append(graph)
    #add types to nodes in graphs!!!
    for graph in graphs:
        new_graph=network_type_specification.turn_gml_graph_to_type_graph(graph)
        result.append(new_graph)
    return result
        
             
    
    
    
if __name__ == '__main__':
    load_graphs_in_folder(None,'/cw/dtaijupiter/NoCsBack/dtai/irma/Martin_experiments/yeast_test/patterns_size_2_proba/patterns_size_2/')
    
        
            
    