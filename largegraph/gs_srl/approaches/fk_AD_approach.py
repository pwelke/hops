'''
Created on Mar 22, 2015

@author: Ravkic
'''
import threading
import argparse,os,pickle
import monitor.process_monitor
import time
from sampling_core import furer_sampling_algorithm as furer
from report_results import furer_report as report
from approaches import prepare_inputs
from approaches import globals_sampling
from OBDs import OBDsearch
import json

def get_nr_embedding(data_graph,pattern,OBdecomp,root_node_predicate_name,monitoring_marks):
    root_nodes = [x for x in data_graph.nodes() if data_graph.node[x]['predicate'] == root_node_predicate_name]
    nr_nodes_data_graph = len(data_graph)
    lock = threading.Lock()
    p=furer.Furer(data_graph,pattern, OBdecomp, root_nodes,None,lock,0,0)
    m = monitor.process_monitor.monitor_process_furer(p, monitoring_marks, lock, 0, nr_nodes_data_graph, len(monitoring_marks), False, None, None, None, None, False)
    mt = threading.Thread(target=m)
    mt.daemon = True
    mt.start()
    p.run()
    estimates = p.FreqValue
    p.abort = True
    return m, estimates

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Running FK-OBD or FK-AD approach')
    parser.add_argument('-d', help='path to data file')
    parser.add_argument('-p', help='path to pattern file')
    parser.add_argument('-o', help='output path')
    parser.add_argument('-exh', help='path to ground truth results (if statistics needed)')
    parser.add_argument('-runs', default=1, type=int, help='Number of iterations. Default=1')
    parser.add_argument('-t', default=300, type=int, help='time interval in seconds')
    parser.add_argument('-max_time', default=36000, type=int, help='maximum sampling time')
    parser.add_argument('-write', default=False, action='store_false',help='save to disk pickles having all the embeddings')
    parser.add_argument('-root_node_id',default=None, type=int,help='id of a root node')
    parser.add_argument('-root_node_name', default=None, help='name of a root node')
    args = parser.parse_args()

    #Preparing the inputs
    data_graph, pattern, OBdecomp, root_node,root_node_predicate_name, interval, max_time, monitoring_marks, root_nodes, Plist= prepare_inputs.prepare_params(args)
    output_folder='fk_AD_results'
    output_path=os.path.join(args.o,output_folder)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if OBdecomp != None:
        OBdecomp_false = [[item] for sublist in OBdecomp for item in sublist]
    else:
        OBdecomp_false = OBDsearch.get_flatList(pattern, startNode=root_node)

    #Main procedure
    monitoring_reports = {}
    all_furer_times = []
    fudicts = []
    average_time = 0
    start = time.time()
    
    m, estimates = get_nr_embedding(data_graph, pattern, OBdecomp_false, root_node_predicate_name, monitoring_marks)
    
    end = time.time()
    average_time += end - start
    fdictionaries_Furer = globals_sampling.globalist_furer
    times_Furer = globals_sampling.globaltimes_furer[1:]
    all_furer_times.append(times_Furer)
    fudicts.append(fdictionaries_Furer)
    monitoring_reports[0] = m.report_structures
    average_time = average_time / args.runs


    #Reporting off
    if args.write == True:
        # write down fudicts
        pickout = open(os.path.join(output_path, 'fudicts.pickle'), 'wb')
        pickle.dump(fudicts, pickout)
        pickout.close()
        # write down monitoring reports
        pickout = open(os.path.join(output_path, 'monitoring_reports.pickle'), 'wb')
        pickle.dump(monitoring_reports, pickout)
        pickout.close()
        # write down furer times
        pickout = open(os.path.join(output_path, 'all_furer_times.pickle'), 'wb')
        pickle.dump(all_furer_times, pickout)
        pickout.close()
        

    # write down monitoring marks
    pickout = open(os.path.join(output_path, 'monitoring_marks.pickle'), 'wb')
    pickle.dump(monitoring_marks, pickout)
    pickout.close()
    #write down Plist
    pickout = open(os.path.join(output_path,'Plist.pickle'), 'wb')
    pickle.dump(Plist, pickout)
    pickout.close()
    
    if False:
       with open(output_path + 'results.out', 'wb') as f:
           out = json.dumps(estimates)
           f.write(out)
    #pickout = gzip.open(os.path.join(output_path,'estimates.pickle'), 'wb')
    #pickle.dump(estimates, pickout)
    #pickout.close()

    with open(output_path + "/average_running_time.res", 'w') as f:
        f.write("Average running time over" + str(args.runs) + " runs: " + str(average_time) + " seconds\n")
    report.main_hops(args.p,output_folder,args.o, args.d, False, args.write, monitoring_reports, data_graph, pattern)
