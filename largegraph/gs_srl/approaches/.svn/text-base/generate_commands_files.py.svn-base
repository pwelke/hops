'''
Created on Aug 2, 2015

@author: irma
'''
import argparse,os

def main(level,init_batch,end_batch,result_path,template):
    counter=init_batch
    if os.path.exists(os.path.join(result_path,'sampling')):
        os.remove(os.path.join(result_path,'sampling'))
    if not os.path.exists(os.path.join(result_path)):
        os.makedirs(os.path.join(result_path))
    file=open(os.path.join(result_path,'sampling'),'a')
    file.write("#!/bin/bash\n")
    while counter<=end_batch:
            file.write(replace_level_batch(level, counter, template))
            counter+=1
    file.close()

def replace_level_batch(level,batch,template):
    linestring = open(template, 'r').read()
    print linestring
    new_string=linestring.replace("NBATCH",str(batch)).replace("LEVEL",level).replace("PREV_B",str(batch-1))
    return new_string


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-level',help='path to patterns of previous batch')
    parser.add_argument('-init_batch',type=int,help='level of the current batchi-ing')
    parser.add_argument('-end_batch',type=int,help='number of previous batch')
    parser.add_argument('-result',help='output of the new batch (no need to specify "batch" in the parameter')
    parser.add_argument('-template',help='output of the new batch (no need to specify "batch" in the parameter')

    args = parser.parse_args()
    main(args.level,args.init_batch,args.end_batch,args.result,args.template)
