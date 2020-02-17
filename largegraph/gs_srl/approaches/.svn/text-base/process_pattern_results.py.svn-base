'''
Created on Jun 9, 2015

@author: irma
'''
import glob
import argparse,os
import pickle
def process_results_for_pattern(results_monitoring):
    files=os.listdir(results_monitoring)
    sorted_files = sorted(files, key=lambda x: int(x.split('_')[2].replace(".info","")))
    x=[]
    for filename in sorted_files:
        #extract the monitoring interval
        x.append(int(filename.split('_')[2].replace(".info","")))
        KLD,bhatta,hellinger,Nr_iterations,nr_embeddings,avg_emb_found,stdev_embeddings=parse_result_file_monitoring(os.path.join(results_monitoring,filename))
        print "KLD: ",KLD
        print "Bhatta: ",bhatta
        print "Hellinger: ",hellinger
        print "nr sampling iterations: ",Nr_iterations
        print "Nr embeddings: ",nr_embeddings
        print "Avg nr. embeddings found: ",avg_emb_found
        print "STDEV embeddings found: ",stdev_embeddings
        print "-----------------------------------------------------------"
    

    
    
    
def parse_result_file_monitoring(file_path):
    KLD=-1
    Nr_iterations=-1
    avg_emb_found=-1
    nr_embeddings=-1
    stdev_embeddings=-1
    bhatta=-1
    hellinger=-1
    
    with open(file_path,'r') as file:
        for line in file.readlines():
            if line.startswith("average KLD"):
                KLD=float(line.split(" ")[4])
                continue
            if line.startswith("average bhatta"):
                bhatta=float(line.split(" ")[4])
            if line.startswith("average hellinger"):
                hellinger=float(line.split(" ")[4])
            if line.startswith("number of sampling iterations"):
                Nr_iterations=int(line.split(" ")[4].replace(":",""))
            if line.startswith("sum of embeddings"):
                nr_embeddings=int(line.split(" ")[3].replace(":",""))
            if line.startswith("average of embeddings"):
                avg_emb_found=float(line.split(" ")[5].replace("iterations:","").rstrip())
            if line.startswith("stdeviation"):
                stdev_embeddings=float(line.split(" ")[3].replace("embeddings:",""))
        return KLD,bhatta,hellinger,Nr_iterations,nr_embeddings,avg_emb_found,stdev_embeddings
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-monitoring', help='wehrre monitoring results are for this patterns')
    parser.add_argument('-results', help='where to store processings of the monitoring')


    args = parser.parse_args()   
    process_results_for_pattern(args.monitoring)  