'''
Created on Feb 15, 2016

@author: irma
'''
import argparse,os,pickle

parser = argparse.ArgumentParser(description='check interupted data')
parser.add_argument('-r', help='path to file with interrupted data')
args = parser.parse_args() 

incomplete=[]
monitoring_reports_120=[]
nr_interrupted=0
print args.r
with open(args.r,'r') as f:
    counter=0
    for line in f.readlines():
        print "Line: ",line
        counter+=1
        if counter==1:
            continue
        nr_interrupted+=1
        path_to_results=line.split(",")[3]
        script=line.split(",")[0]
        result=None
        if "furer_sampling_approach.py" in script:
            result="results_furer"
        if "random_vertex_sampling_approach.py" in script:
            result="random_vertex_approach"
        if "false_furer_sampling_approach.py" in script:
            result="results_false_furer"
        if "exhaustive_approach.py" in script:
            result="exhaustive_approach"
        print path_to_results,"result folder: ",result
        if not os.path.exists(os.path.join(path_to_results,result,'complete.info')):
            incomplete.append(path_to_results+"/"+result)
            if os.path.exists(os.path.join(path_to_results,result,'monitoring_reports.pickle')):
                 pkl_file = open(os.path.join(path_to_results,result,'monitoring_reports.pickle'), 'rb')
                 monitoring_reports=pickle.load(pkl_file)  
                 if len(monitoring_reports)==120:
                     monitoring_reports_120.append(path_to_results+"/"+result)

print "Nr interrupted fileS: ",nr_interrupted
print "Nr incomplete results",len(incomplete)
for i in incomplete:
    print i
print "Nr incomplete, but fully monitored jobs"
for i in monitoring_reports_120:
    print i
            
