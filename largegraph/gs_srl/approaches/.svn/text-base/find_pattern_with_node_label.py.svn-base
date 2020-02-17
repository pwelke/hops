'''
Created on Jul 30, 2015

@author: irma
'''
'''
Created on Jul 13, 2015

@author: irma
'''
import argparse,os
import networkx as nx

def parse_command(command):
    split_string=command[0].split(" ")
    resulting_string=[]
    for i in xrange(0,len(split_string)):
        if split_string[i]=="-data_graph_path":
            resulting_string.insert(0, split_string[i+1]+",")
        if split_string[i]=="-pattern_path":
            resulting_string.insert(1, split_string[i+1]+",")
        if split_string[i]=="-output_path":
            resulting_string.insert(2, split_string[i+1]+",")
        if split_string[i]=="-exhaustive_approach_results_path":
            resulting_string.insert(3, split_string[i+1]+",")
        if split_string[i]=="-runs":
            resulting_string.insert(4, split_string[i+1]+",")
        if split_string[i]=="-time_interval":
            resulting_string.insert(5, split_string[i+1]+",")
        if split_string[i]=="-max_time":
            resulting_string.insert(6, split_string[i+1]) 
    return ''.join(resulting_string)

def make_interrupted_files_param(results,not_finished_commands):
    file=open(os.path.join(results,'interrupted.data'),'w')
    file.write("data_graph_path,pattern_path,output_path,exhaustive_approach_results_path,runs,time_interval,max_time\n")
    for command in not_finished_commands:
        file.write(parse_command(command)+"\n")
    file.close()
    print "file saved to: ",os.path.join(results,'interrupted.data')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-patterns', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-label', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')

    args = parser.parse_args() 
    results=args.patterns
    level=results.split("/")[-2].split("_")[-1]
    pattern_containing_node=[]
    
    for dir in os.listdir(results):
        #go through batches
        if dir.startswith("batch"):
            print "BATCHES"
            for pattern_res in os.listdir(os.path.join(results,dir)):
                
                result_to_batch=os.path.join(results,dir,pattern_res)
                if os.path.isfile(result_to_batch):
                    continue
                patt=nx.read_gml(os.path.join(result_to_batch,pattern_res+".gml"))
                for node in patt.nodes():
                    if patt.node[node]['label']==args.label:
                        pattern_containing_node.append(result_to_batch)
                        break
    
    print "Patterns containing this label:"
    for p in pattern_containing_node:
        print p
                
            
    
    



        

        
    
        
        
            
            
            