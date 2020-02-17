'''
Created on Jun 30, 2015

@author: irma
'''
import argparse,pickle,os,sys
import networkx as nx
from report_results import report_exhaustive_approach as report
from report_results import make_selected_results_csv as csv_report
import shutil


def exhaustive_report(output_path,pattern_path):
    #load monitoring marks
    monitoring_path=os.path.join(output_path,'monitoring')
    if os.path.exists(monitoring_path):
        shutil.rmtree(monitoring_path)
    pkl_file = open(os.path.join(output_path,'monitoring_marks.pickle'), 'rb')
    monitoring_marks=pickle.load(pkl_file)  
    
    pkl_file = open(os.path.join(output_path,'monitoring_reports.pickle'), 'rb')
    monitoring_reports=pickle.load(pkl_file)  
    if not os.path.exists(monitoring_path):
        os.makedirs(monitoring_path)
        
    report.report_results_exhaustive_monitoring(monitoring_reports, monitoring_marks, monitoring_path)
    row=csv_report.get_row_exhaustive(output_path, output_path,pattern_path)
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
