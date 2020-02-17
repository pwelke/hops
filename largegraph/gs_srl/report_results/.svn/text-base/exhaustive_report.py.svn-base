'''
Created on Jun 30, 2015

@author: irma
'''
import argparse,pickle,os,sys
import networkx as nx
import report_exhaustive_approach as report
import make_selected_results_csv as csv_report
import shutil


def exhaustive_report(result,redo):
    print "Doing exhaustive reporting for",result
    output_path=os.path.join(result,"exhaustive_approach")
    #load monitoring marks
    monitoring_path=os.path.join(output_path,'monitoring')
    if redo and os.path.exists(monitoring_path):
        shutil.rmtree(monitoring_path) 
    if (not redo) and os.path.exists(monitoring_path) and len(os.listdir(monitoring_path))>=0:
        print "Results already post-processed"
        with open(os.path.join(output_path,"monitored.info"),'w') as f:
            f.write("monitored")
        row=csv_report.get_row_exhaustive(result, output_path, result.replace("RESULTS","PATTERNS"))
        with open(os.path.join(output_path,"exhaustive_info_row.info"),'w') as f:
            f.write(str(row))
        
        sys.exit()
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    
    pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
    monitoring_reports=pickle.load(pkl_file)  
    print "loaded monitoring_reports ..."
    print "Nr reports: ",len(monitoring_reports)
    if not os.path.exists(monitoring_path):
        os.makedirs(monitoring_path)
        
    report.report_results_exhaustive_monitoring(monitoring_reports, monitoring_marks, monitoring_path)
    row=csv_report.get_row_exhaustive(result, output_path,result.replace("RESULTS","PATTERNS"))
    with open(os.path.join(output_path,"exhaustive_info_row.info"),'w') as f:
        f.write(str(row))
    
    with open(os.path.join(output_path,"monitored.info"),'w') as f:
        f.write("monitored")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-result',help='path to results for a pattern')
    parser.add_argument('-data',help='path to data graph')
    parser.add_argument('-redo',default=False,action='store_true',help='redo report')
    args = parser.parse_args()
    exhaustive_report(args.result,args.redo)
