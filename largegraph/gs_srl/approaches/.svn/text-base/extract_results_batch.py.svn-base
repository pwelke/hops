'''
Created on May 6, 2015

@author: irma
'''
import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-path_to_results', metavar='N',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-path_to_patterns', metavar='N',help='this is a general path containing patterns')
    parser.add_argument('-N',help='select N best patterns - by some criterium')
    parser.add_argument('-copy_files',default=True,help='select N best patterns - by some criterium')

    args = parser.parse_args()
    
    #Extract results for each method
    #Make csv with average times
    
    path_to_selected_results=os.path.join(os.path.dirname(os.path.dirname(args.path_to_results)),'selected_results')
    
    if(not os.path.exists(path_to_selected_results)):
        os.makedirs(path_to_selected_results)    
        
    #get path of all results that have exhausted approach results
    patterns_with_success_results_path=[]
    pattern_names_with_succes=[]
    
    for dir in os.listdir(args.path_to_results):
        pattern_directory=os.path.join(args.path_to_results,dir)
        pattern_name=dir
        exhaustive_dir=os.path.join(pattern_directory,'exhaustive_approach')
        
        for file in os.listdir(exhaustive_dir):
            print "FILE: ",file
            if file=="no_results.info":
              break
            else:
              pattern_names_with_succes.append(pattern_name)
              patterns_with_success_results_path.append(pattern_directory)
              break
                
        
        
        #print exhaustive_dir
                                  
    print "Number of successful patterns: ",len(pattern_names_with_succes)                                                  
                                               