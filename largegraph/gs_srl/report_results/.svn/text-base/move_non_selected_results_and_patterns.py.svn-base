'''
Created on Nov 25, 2015

@author: irma
'''
import argparse,os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-results_path',help='path to results for a pattern')
    parser.add_argument('-redo',default=False,action='store_true',help='redo report')
    
    args = parser.parse_args()
    general_copy_destination_dtaijupiter="irma@spock.cs.kuleuven.be:/cw/dtaijupiter/NoCsBack/dtai/MARTIN_SAMPLING_BACKUP/"
    for batch in os.listdir(args.results_path):
        print batch
        if not batch.startswith("batch"):
            continue
        else:
            for pattern_res in os.listdir(os.path.join(args.results_path,batch)):
                print pattern_res
                result_to_batch=os.path.join(args.results_path,batch,pattern_res)
                if os.path.exists(os.path.join(result_to_batch,'selected.info')):
                    continue
                else:
                    subpath=result_to_batch.split("/")[5:]
                    print "Subpath: ",subpath
                    print "Will Copy result: ",result_to_batch,"to",general_copy_destination_dtaijupiter+'/'.join(subpath)
            
