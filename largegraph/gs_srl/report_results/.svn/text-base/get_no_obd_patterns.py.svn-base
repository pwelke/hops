'''
Created on Mar 28, 2016

@author: irma
'''
import os

path_to_results="/cw/dtaijupiter/NoCsBack/dtai/irma/MARTIN_EXPERIMENTS_BACKUP/RESULTS_DBLP/RESULTS_400_BATCH/"
overall_patt=0
no_obd_patt=0

for patt_size in os.listdir(path_to_results):
    if not os.path.isdir(os.path.join(path_to_results,patt_size)):
        continue
    for batch in os.listdir(os.path.join(path_to_results,patt_size)):
        if not os.path.isdir(os.path.join(path_to_results,patt_size,batch)) and not batch.startswith("batch"):
            continue
        for patt in os.listdir(os.path.join(path_to_results,patt_size,batch)):
            pattern=os.path.join(path_to_results,patt_size,batch,patt)
            if os.path.exists(os.path.join(pattern,'selected.info')):
               overall_patt+=1
               if os.path.exists(os.path.join(pattern,'results_furer','no_obdecomp.info')):
                   no_obd_patt+=1
print no_obd_patt,overall_patt
print no_obd_patt/float(overall_patt)*100
                
