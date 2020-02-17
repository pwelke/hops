import threading
import argparse, os, time, pickle
import monitor.process_monitor
import report_results.report_exhaustive_approach as end_report
import report_results.exhaustive_report as report
from sampling_core import exhaustive_approach
from report_results import NoResults_exception
from approaches import prepare_inputs
from approaches import globals_sampling

def get_nr_embeddings(data_graph,pattern,OBdecomp,root_nodes,monitoring_marks):
    plist = [item for sublist in OBdecomp for item in sublist]
    lock = threading.Lock()
    p = exhaustive_approach.Exhaustive_approach(data_graph, pattern, plist, root_nodes, None, lock)
    m = monitor.process_monitor.monitor_process_exhaustive(p, monitoring_marks, lock, None)
    mt = threading.Thread(target=m)
    mt.daemon = True
    mt.start()
    p.run()
    p.abort = True
    return m


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-d', help='path to data file')
    parser.add_argument('-p', help='path to pattern file')
    parser.add_argument('-o', help='output path')
    parser.add_argument('-exh', help='path to ground truth results (if statistics needed)')
    parser.add_argument('-runs', default=1, type=int, help='Number of iterations. Default=1')
    parser.add_argument('-t', default=None, type=int, help='time interval in seconds')
    parser.add_argument('-max_time', type=int, help='maximum sampling time')
    parser.add_argument('-root_node_id', default=None, type=int, help='id of a root node')
    parser.add_argument('-root_node_name', default=None, help='name of a root node')

    print("Running exhaustive approach")
    args = parser.parse_args()
    if args.t == None:
        args.t = args.max_time
    data_graph, pattern, OBdecomp, root_node,root_node_predicate_name, interval, max_time, monitoring_marks, root_nodes, Plist= prepare_inputs.prepare_params(args)
    output_path=os.path.join(args.o, 'exhaustive_results')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    #Main procedure
    start = time.time()
    m=get_nr_embeddings(data_graph, pattern, OBdecomp, root_nodes, monitoring_marks)
    end = time.time()
    if m.timeout:
        with open(args.o + "/timeout.info", 'w') as f:
            f.write("exhaustive finished with timeout!")
    try:
        end_report.report_results_exhaustive(globals_sampling.freq_dict_exhaustive,
                                     globals_sampling.temporary_observed[0], output_path, start, end, Plist,
                                     "final_result")

    except NoResults_exception:
        with open(output_path + "/no_results.info", 'w') as f:
            print("fudicts is empty!: No results for this pattern: " + args.p)
            f.write("no results for this pattern!, fudicts is empty!")

    pickout = open(os.path.join(output_path, 'monitoring_reports.pickle'), 'wb')
    pickle.dump(m.report_structures, pickout)
    pickout.close()

    pickout = open(os.path.join(output_path, 'fudict.pickle'), 'wb')
    pickle.dump(globals_sampling.freq_dict_exhaustive, pickout)
    pickout.close()

    # write down monitoring marks
    pickout = open(os.path.join(output_path, 'monitoring_marks.pickle'), 'wb')
    pickle.dump(monitoring_marks, pickout)
    pickout.close()

    report.exhaustive_report(output_path,args.p)