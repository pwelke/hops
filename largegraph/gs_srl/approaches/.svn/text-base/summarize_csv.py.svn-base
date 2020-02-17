'''
Created on May 30, 2015

@author: irma
'''
import argparse,csv
import CSV_REPORT as csv_report
import numpy

def main(csv_file):
    nr_randvar_values_avg_emb_exhaustive={}
    nr_randvar_values_avg_emb_random={}
    nr_randvar_values_avg_emb_furer={}
    nr_randvar_values_avg_emb_false_furer={}
    
    nr_randvar_values_time_exhaustive={}
    nr_randvar_values_time_random={}
    nr_randvar_values_time_furer={}
    nr_randvar_values_time_false_furer={}
    
    nr_targets_avg_emb_exhaustive={}
    nr_targets_avg_emb_random={}
    nr_targets_avg_emb_furer={}
    nr_targets_avg_emb_false_furer={}
    
    nr_targets_time_exhaustive={}
    nr_targets_time_random={}
    nr_targets_time_furer={}
    nr_targets_time_false_furer={}
    
    cycles_avg_emb={}
    
    missing_run_times_exhaustive=[]
    missing_run_times_random=[]
    missing_run_times_furer=[]
    missing_run_times_false_furer=[]
    
    with open(csv_file,"r") as csv_file:
        reader=csv.DictReader(csv_file)
        for row in reader:
            #if validRow(row)==False:
            #    continue
            if not row["nr_randvar_values"] in nr_randvar_values_avg_emb_exhaustive.keys():
                nr_randvar_values_avg_emb_exhaustive[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_avg_emb_random.keys():
                nr_randvar_values_avg_emb_random[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_avg_emb_furer.keys():
                nr_randvar_values_avg_emb_furer[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_avg_emb_false_furer.keys():
                nr_randvar_values_avg_emb_false_furer[row["nr_randvar_values"]]=[]
                
            if not row["nr_randvar_values"] in nr_randvar_values_time_exhaustive.keys():
                nr_randvar_values_time_exhaustive[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_time_random.keys():
                nr_randvar_values_time_random[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_time_furer.keys():
                nr_randvar_values_time_furer[row["nr_randvar_values"]]=[]
            if not row["nr_randvar_values"] in nr_randvar_values_time_false_furer.keys():
                nr_randvar_values_time_false_furer[row["nr_randvar_values"]]=[]
                    
                
            if not row["nr_targets"] in nr_targets_avg_emb_exhaustive.keys():
                nr_targets_avg_emb_exhaustive[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_avg_emb_random.keys():
                nr_targets_avg_emb_random[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_avg_emb_furer.keys():
                nr_targets_avg_emb_furer[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_avg_emb_false_furer.keys():
                nr_targets_avg_emb_false_furer[row["nr_targets"]]=[]
                
            if not row["nr_targets"] in nr_targets_time_exhaustive.keys():
                nr_targets_time_exhaustive[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_time_random.keys():
                nr_targets_time_random[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_time_furer.keys():
                nr_targets_time_furer[row["nr_targets"]]=[]
            if not row["nr_targets"] in nr_targets_time_false_furer.keys():
                nr_targets_time_false_furer[row["nr_targets"]]=[]
            
           
           
           
            if row['exh_emb']!='N':
                nr_randvar_values_avg_emb_exhaustive[row["nr_randvar_values"]].append(int(row['exh_emb']))
                nr_randvar_values_time_exhaustive[row["nr_randvar_values"]].append(float(row['exh_rt']))
                nr_targets_avg_emb_exhaustive[row["nr_targets"]].append(int(row['exh_emb']))
                nr_targets_time_exhaustive[row["nr_targets"]].append(float(row['exh_rt']))
            if row['limit16_rnd_emb']!='NC':
                nr_randvar_values_avg_emb_random[row["nr_randvar_values"]].append(int(row['limit16_rnd_emb']))
                nr_targets_avg_emb_random[row["nr_targets"]].append(int(row['limit16_rnd_emb']))
            
            if  row['rnd_avgRT_16']!='NC':
                nr_randvar_values_time_random[row["nr_randvar_values"]].append(float(row['rnd_avgRT_16']))
                nr_targets_time_random[row["nr_targets"]].append(float(row['rnd_avgRT_16']))
            if row['limit16_rnd_emb']!='NC' and row['rnd_avgRT_16']=='NC':
                missing_run_times_random.append(row["pattern_name"])
            
            if row['limit16_fur_emb']!='NC':
                nr_randvar_values_avg_emb_furer[row["nr_randvar_values"]].append(int(row['limit16_fur_emb']))
                nr_targets_avg_emb_furer[row["nr_targets"]].append(int(row['limit16_fur_emb']))

            if row['furer_avgRT_16']!='NC':
                nr_randvar_values_time_furer[row["nr_randvar_values"]].append(float(row['furer_avgRT_16']))
                nr_targets_time_furer[row["nr_targets"]].append(float(row['furer_avgRT_16']))
            if row['limit16_fur_emb']!='NC' and row['furer_avgRT_16']=='NC':
                 missing_run_times_furer.append(row["pattern_name"])
                
            if row['limit16_ff_emb']!='NC':
                 nr_randvar_values_avg_emb_false_furer[row["nr_randvar_values"]].append(int(row['limit16_ff_emb']))
                 nr_targets_avg_emb_false_furer[row["nr_targets"]].append(int(row['limit16_ff_emb']))
            if row['ff_avgRT_16']!='NC':
                nr_randvar_values_time_false_furer[row["nr_randvar_values"]].append(float(row['ff_avgRT_16'])) 
                nr_targets_time_false_furer[row["nr_targets"]].append(float(row['ff_avgRT_16']))
            if row['limit16_ff_emb']!='NC' and row['ff_avgRT_16']=='NC':
                missing_run_times_false_furer.append(row["pattern_name"])
 

    
    #process nr randvar values to avg embeddings
    print nr_randvar_values_avg_emb_exhaustive
    exh_min_max=find_max_min(nr_randvar_values_avg_emb_exhaustive)
    rnd_min_max=find_max_min(nr_randvar_values_avg_emb_random)
    furer_min_max=find_max_min(nr_randvar_values_avg_emb_furer)
    ffurer_min_max=find_max_min(nr_randvar_values_avg_emb_false_furer)
    
    time_exh_min_max=find_max_min(nr_randvar_values_time_exhaustive)
    time_rnd_min_max=find_max_min(nr_randvar_values_time_random)
    time_furer_min_max=find_max_min(nr_randvar_values_time_furer)
    time_ffurer_min_max=find_max_min(nr_randvar_values_time_false_furer)
    
    to_average_and_std(nr_randvar_values_avg_emb_exhaustive)
    to_average_and_std(nr_randvar_values_avg_emb_random)
    to_average_and_std(nr_randvar_values_avg_emb_furer)
    to_average_and_std(nr_randvar_values_avg_emb_false_furer)
    
    #process nr target values to avg embeddings
    t_exh_min_max=find_max_min(nr_targets_avg_emb_exhaustive)
    t_rnd_min_max=find_max_min(nr_targets_avg_emb_random)
    t_furer_min_max=find_max_min(nr_targets_avg_emb_furer)
    t_ffurer_min_max=find_max_min(nr_targets_avg_emb_false_furer)
    to_average_and_std(nr_targets_avg_emb_exhaustive)
    to_average_and_std(nr_targets_avg_emb_random)
    to_average_and_std(nr_targets_avg_emb_furer)
    to_average_and_std(nr_targets_avg_emb_false_furer)
    
    time_t_exh_min_max=find_max_min(nr_targets_time_exhaustive)
    time_t_rnd_min_max=find_max_min(nr_targets_time_random)
    time_t_furer_min_max=find_max_min(nr_targets_time_furer)
    time_t_ffurer_min_max=find_max_min(nr_targets_time_false_furer)
    
    
    
    report=csv_report.CSV_REPORT()
    report.set_nr_randvar_values_avg_emb_exhaustive(nr_randvar_values_avg_emb_exhaustive)
    report.set_nr_randvar_values_avg_emb_random(nr_randvar_values_avg_emb_random)
    report.set_nr_randvar_values_avg_emb_furer(nr_randvar_values_avg_emb_furer)
    report.set_nr_randvar_values_avg_emb_false_furer(nr_randvar_values_avg_emb_false_furer)
    report.set_nr_randvar_values_min_max_exhaustive(exh_min_max)
    report.set_nr_randvar_values_min_max_random(rnd_min_max)
    report.set_nr_randvar_values_min_max_furer(furer_min_max)
    report.set_nr_randvar_values_min_max_false_furer(ffurer_min_max)
    report.set_time_nr_randvar_values_min_max_exhaustive(time_exh_min_max)
    report.set_time_nr_randvar_values_min_max_random(time_rnd_min_max)
    report.set_time_nr_randvar_values_min_max_furer(time_furer_min_max)
    report.set_time_nr_randvar_values_min_max_false_furer(time_ffurer_min_max)
    
    report.set_nr_targets_avg_emb_exhaustive(nr_targets_avg_emb_exhaustive)
    report.set_nr_targets_avg_emb_random(nr_targets_avg_emb_random)
    report.set_nr_targets_avg_emb_furer(nr_targets_avg_emb_furer)
    report.set_nr_targets_avg_emb_false_furer(nr_targets_avg_emb_false_furer)
    report.set_nr_targets_min_max_exhaustive(t_exh_min_max)
    report.set_nr_targets_min_max_random(t_rnd_min_max)
    report.set_nr_targets_min_max_furer(t_furer_min_max)
    report.set_nr_targets_min_max_false_furer(t_ffurer_min_max)
    report.set_time_nr_targets_min_max_exhaustive(time_t_exh_min_max)
    report.set_time_nr_targets_min_max_random(time_t_rnd_min_max)
    report.set_time_nr_targets_min_max_furer(time_t_furer_min_max)
    report.set_time_nr_targets_min_max_false_furer(time_t_ffurer_min_max)
    
    print "Missing rt time random: ",len(missing_run_times_random)
    print "Missing rt furer: ",len(missing_run_times_furer)
    print "Missing rt false furer: ",len(missing_run_times_false_furer)
    
    print "MISSING RT FURER PATTERNS: "
    
    
    print report


def get_float_value(row,key):
    try:
        return float(row[key])
    except ValueError:
        return 

def validRow(row):
    for key in row.keys():
        if row[key]=='NC' or row[key]=='NC +- NC' or row[key]=='C' or row[key]=='N':
            return False
    return True

    
def find_max_min(results):
    res={}
    for k in results.keys():
         if len(results[k])==0:
             res[k]=(float('nan'),float('nan'))
         else:
             res[k]=(min(results[k]),max(results[k]))
    return res
            
                
def to_average_and_std(results):
    for k in results.keys():
        results[k]=(numpy.average(results[k]),numpy.std(results[k]))

              
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-csv', help='this is a general path to results for patterns(containing results for exhaustive, random sampling, furer and false furer')
    args = parser.parse_args() 
    main(args.csv)
    
