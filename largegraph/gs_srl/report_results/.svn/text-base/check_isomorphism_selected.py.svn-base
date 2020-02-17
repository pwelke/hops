'''
Created on Aug 9, 2015

@author: irma
'''
import argparse,os
import networkx as nx
import patternGenerator.generate_pattern as gen_pat

def main(results,patterns,pattern):
    selected_patterns_paths=[]
    print "RESULTS: ",results
    #collect all selected patterns
    if results!=None:
        for dir in os.listdir(results):
                #go through batches
                if dir.startswith("batch"):
                    #print "BATCHES"
                    for pattern_res in os.listdir(os.path.join(results,dir)):
                        result_to_batch=os.path.join(results,dir,pattern_res)   
                        if os.path.exists(os.path.join(result_to_batch,'selected.info')):
                            selected_patterns_paths.append(os.path.join(patterns,dir,pattern_res,pattern_res+".gml"))
    else:
                    for pattern_res in os.listdir(os.path.join(patterns)):
                        if os.path.isfile(os.path.join(patterns,pattern_res)):
                          continue
                        if os.path.isfile(os.path.join(patterns,pattern_res)):
                            continue
                        result_to_batch=os.path.join(patterns,pattern_res)   
                        selected_patterns_paths.append(os.path.join(patterns,pattern_res,pattern_res+".gml"))
    print "# SELECTED GRAPHS: ",len(selected_patterns_paths)
    #load graphs
    graphs=[]
    counter=1
    for pattern_path in selected_patterns_paths:
        graphs.append(nx.read_gml(pattern_path))
        print "Loaded: ",counter, "th graph"
        counter+=1
    if pattern!=None:
        additional_graph=nx.read_gml(pattern)
        graphs.append(additional_graph)    
    filtered_list,list_for_removal,pairs=gen_pat.find_isomorphic_graphs(graphs)
    if(len(filtered_list)==len(graphs)):
        print "No isomorphic graphs! phew!!!"
        return False
    for pair in pairs.keys():
        print "*******************************"
        print selected_patterns_paths[pair]
        print "and "
        print selected_patterns_paths[pairs[pair]]
    print "Number of isomorphic: ",len(list_for_removal)
    for ind in list_for_removal:
        print selected_patterns_paths[ind]
    return True  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-patterns',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    
    args = parser.parse_args()   
    print args.results
    main(args.results,args.patterns,None) 
