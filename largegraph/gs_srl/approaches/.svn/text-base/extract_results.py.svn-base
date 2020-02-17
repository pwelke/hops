'''
Created on May 25, 2015

@author: irma
'''
import argparse
import os
import create_csv_batch_file
import filter_batch_results
import create_new_batch

def get_batch_paths(path_results):
    tmp=[]
    for dir in os.listdir(path_results):
        if dir.startswith("batch"):
          tmp.append(dir)
    return tmp  

def make_csv_batch(batc_path,folder_output):
    print "Creating csv file ...at",batc_path
    create_csv_batch_file.makecsv_file_for_final_limits(batc_path, folder_output,True)
    
def select_results_for_batch(batch_csv_file,patterns,path_to_results,output_selected_files,level):
    return filter_batch_results.main(batch_csv_file,patterns,path_to_results, 400, output_selected_files, level)

def main(results,redo,create_batch_flag,data_label):
    #Given path to results go over all batch results
    #get all batch paths
    batch_paths=get_batch_paths(results)
    level=results.split("/")[-2].split("_")[-1]
    #general path for experiments for this result
    #make info folder for these experiments
    for batch in batch_paths:
        #make csv result for this batch
        make_csv_batch(os.path.join(results,batch),results)
        #select results for this batch
    batch_csv_file=os.path.join(results,"csv_results")
    #Select results
    nr_selected,batch_number=select_results_for_batch(batch_csv_file,results,results,results,level)
    latest_batch=batch_paths[-1].split("batch")[1]
    #make file with selected results
    print os.path.join(results,str(nr_selected))+"_selected"
    with open(os.path.join(results,str(nr_selected)+"_selected"),'w') as f:
        f.write(str(nr_selected))     
    if create_batch_flag==True and (nr_selected<400):
         output='/'.join(args.patterns.split("/")[0:-2])
         #make a new batch
         create_new_batch.main(args.patterns, int(level), int(latest_batch), output, data_label)
         
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results', metavar='N',help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    parser.add_argument('-redo',default=False,action='store_true',help='in case results already processed for this batch redo is false by default unless specified true')
    parser.add_argument('-cb',default=False,action='store_true',help='in case results already processed for this batch redo is false by default unless specified true')
    parser.add_argument('-data_label',help='in case results already processed for this batch redo is false by default unless specified true')

    args = parser.parse_args() 
    main(args.results,args.redo,args.cb,args.data_label)
