'''
Created on May 26, 2015

@author: irma
'''
import argparse,os
import create_csv_batch_file
import filter_batch_results
#import batch_info,create_csv_batch_file
#import filter_batch_results,csv
import generate_commands_for_reporting
import get_patterns_info

def remove_files(list):
    for l in list:
        if os.path.exists(l):
            os.remove(l)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-patterns',help='in case results already processed for this batch redo is false by default unless specified true')
    parser.add_argument('-data',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-path_to_reporting_scripts',help='path to reporting scripts')
    parser.add_argument('-csv',default=False,action='store_true',help='make csv files')
    parser.add_argument('-filter',default=False,action='store_true',help='select N results')
    parser.add_argument('-N',default=400,type=int,help='number of patterns to be selected')
    parser.add_argument('-N_LIMITS',type=int,default=16,help='number of n limits')
    parser.add_argument('-n',type=int,help='number of nodes in the data graph')
    parser.add_argument('-existing_csv',default=None,help='path to existing csv')

    args = parser.parse_args() 
    
    results=args.results
    pattern_path=args.patterns
    level=results.split("/")[-2].split("_")[-1]
    nr_patterns_to_be_selected=args.N
    nlimits=args.N_LIMITS
    n=args.n
    selected_patterns=[]
    
    if args.filter==True:
        args.csv=True
    
    for dir in os.listdir(results):
        print "BATCHES"
        #go through batches
        if dir.startswith("batch"):
            print "***************************",dir,"*****************"
            #result to batch
            result_to_batch=os.path.join(results,dir)
            
            patterns_for_batch=os.path.join(pattern_path,dir)
            if not os.path.exists(os.path.join(patterns_for_batch,'selected.info')):
                continue
            #batch_info.main(result_to_batch, True, patterns_for_batch,nlimits)
            #create csv file
            pattern_paths=os.path.join(args.results,dir)
            patterns=os.path.join(args.patterns,dir)
            output_path=args.results
            if args.csv and args.existing_csv==None:
                csv_file=create_csv_batch_file.makecsv_file_for_final_limits(pattern_paths, output_path, True)
            else:
                #load existing csv file
                csv_file=args.existing_csv
            #Filter results
            if args.filter:
                nr_selected,batch,selected=filter_batch_results.main(csv_file, pattern_paths, result_to_batch, nr_patterns_to_be_selected, output_path, level,n)
                nr_patterns_to_be_selected-=nr_selected
                selected_patterns.extend(selected)
            print "**********************************************************"
            #make charactersitics of graphs csv (only using patterns data)
            csv_file_characteristics=get_patterns_info.graph_characteristics_csv(patterns, output_path)
    selected_patterns_paths=[]
    if len(selected_patterns)==args.N:
        if not os.path.exists(os.path.join(args.results,"processing_commands")):
            os.makedirs(os.path.join(args.results,"processing_commands"))
        for patt in selected_patterns:
            path_to_result=os.path.join(args.results,patt[1],patt[0])
            selected_patterns_paths.append(path_to_result)
            
        #generate commands for patterns for the statistics to be reported
        generate_commands_for_reporting.main(args.data,selected_patterns_paths,os.path.join(args.results,"processing_commands"),args.path_to_reporting_scripts)


