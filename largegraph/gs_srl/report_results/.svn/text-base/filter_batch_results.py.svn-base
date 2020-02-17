'''
Created on May 15, 2015
THIS SCRIPT IS USED TO FILTER THE RESULTS OF ALL BATCHES THROUGH CSV FILES.
SO FIRST CALL SCRIPT: CREATE_CSV_BATCH_FILE.PY FOR EACH BATCH.
THEN CALL THIS SCRIPT TO SELECT DESIRED PATTERNS FOR A SPECIFIC LEVEL
@author: irma
'''
import argparse
import os
import csv,shutil,random,sys,math



def select_patterns(path_to_csv,batch_number,n):
    print "Number of nodes in the data graph: ",n
    selected_patterns=[]
    incomplete_patterns=[]
    with open(path_to_csv, 'rb') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                pattern_name=row['pattern_name']
                #here put some condition that Jan decides
                #for now find average of embeddings for all approaches
                if row['exh_emb']=='NC' or row['exh_emb']=='N':
                   incomplete_patterns.append((pattern_name,batch_number))
                else:
                   nr_embeddings=row['exh_emb']
                   #nr_embeddings=int(row['exh_emb'])+int(row['limit16_rnd_emb'])+int(row['limit16_fur_emb'])+int(row['limit16_ff_emb'])
                   #SELECTION CRITERIA JAN R.
                   if math.sqrt(n)<int(nr_embeddings)<=n:
                       selected_patterns.append((pattern_name,batch_number))
    return selected_patterns,incomplete_patterns

#With this option we assume that we let Furer run for 1 hour. In that case 
#CSV file should have a field "selected" when the pattern was selected in Furer
def select_patterns_option2(path_to_csv,batch_number,n):
    print "Number of nodes in the data graph: ",n
    selected_patterns=[]
    incomplete_patterns=[]
    with open(path_to_csv, 'rb') as csvfile:
            reader=csv.DictReader(csvfile)
            for row in reader:
                pattern_name=row['pattern_name']
                if row['selected']=='False':
                   incomplete_patterns.append((pattern_name,batch_number))
                else:
                   selected_patterns.append((pattern_name,batch_number))
    return selected_patterns,incomplete_patterns
                       

def copy_selected_patterns_to_selected_files(selected_patterns,results,output_dir,batch):
   print "RESULTS:",results
   for pattern_name in selected_patterns:
       #make directory with pattern name
       output_dir_pat=os.path.join(output_dir,pattern_name[0])
       if not os.path.exists(output_dir_pat):
           os.makedirs(output_dir_pat)
       #get pattern from exhaustive approach
       pattern_file_path=os.path.join(results,pattern_name[0])
       pattern_file_results=os.path.join(results,pattern_name[0],"exhaustive_approach","input_pattern.gml")
       #copy pattern file to selected results
       #print "Making selected results directory...",output_dir_pat
       #print "Pattern file path...",pattern_file_path
       #print "Pattern file pattern: ",pattern_file_results
       shutil.copy(pattern_file_results,os.path.join(output_dir_pat,pattern_name[0]+".gml"))
       #Create batch number infor for the pattern
      
       with open(os.path.join(output_dir_pat,'batch.info'),'w') as f:
           f.write(pattern_name[1]) 
       with open(os.path.join(output_dir_pat,'pattern_path.info'),'w') as f:
           f.write(pattern_file_results)
           
def mark_selected_patterns_in_results_exhaustive(selected_patterns,results):
    for pattern_name in selected_patterns:
        pattern_file_results=os.path.join(results,pattern_name[0],"exhaustive_approach","selected.info")
        if not os.path.exists(pattern_file_results):
            with open(pattern_file_results,'w') as file:
                file.write("selected")
            

def unmark_selected_patterns_in_results_exhaustive(selected_patterns,results):
    for pattern_name in selected_patterns:
        pattern_file_results=os.path.join(results,pattern_name[0],"exhaustive_approach","selected.info")
        if os.path.exists(pattern_file_results):
            os.remove(pattern_file_results)

def main(path_to_csv_file,patterns,results,N,o,level,n):
    print "Filtering and selecting the results ..."
    all_selected_results=[]
    nr_existing_results=0
    nr_patterns_to_be_selected=N
    #create directory for selected results
    selected_results_dir=os.path.join(o,'selected_results')
    if not os.path.exists(selected_results_dir):
        os.makedirs(selected_results_dir)
    #Go through pattern names in csv file
    #extract batch number
    print "******************************************************************"
    print "Batch csv: ",path_to_csv_file
    batch_number=results.split("/")[-1]
    print "Batch number: ",batch_number
    path_to_csv=path_to_csv_file
    selected_patterns=select_patterns_option2(path_to_csv,batch_number,n)[0]
    print "Number of selected patterns: ",len(selected_patterns)
    print "Path to CSV: ",path_to_csv
    
    #If number of selected patterns bigger than desired, chose random N patterns
    if len(selected_patterns)>=nr_patterns_to_be_selected:
        random.shuffle(selected_patterns)
        selected_patterns=selected_patterns[0:nr_patterns_to_be_selected]
    #If the number of selected patterns is smaller than desired, add them to selected, and update the number of patterns to be selected
    else:
        nr_patterns_to_be_selected=N-len(selected_patterns)
    unmark_selected_patterns_in_results_exhaustive(selected_patterns,results)
    mark_selected_patterns_in_results_exhaustive(selected_patterns,results)
    copy_selected_patterns_to_selected_files(selected_patterns,results,selected_results_dir,batch_number)
    all_selected_results.extend(selected_patterns)                                       
    #Select only a limited number of patterns
    return len(all_selected_results),batch_number.split("batch")[1],selected_patterns
         

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-path_to_csv_files',help='specifies path where csv files are contained')
    parser.add_argument('-results',help='path to results (DONT GIVE A SPECIFIC BATCH)')
    parser.add_argument('-N',type=int,help='select N random results that fit the criteria for selection')
    parser.add_argument('-o', metavar='N',help='this is path to output')
    parser.add_argument('-level', metavar='N',type=int,help='pattern_level')

    args = parser.parse_args()
    main(args.path_to_csv_files, args.results, args.N,args.o,args.level)
        
            
    
    
