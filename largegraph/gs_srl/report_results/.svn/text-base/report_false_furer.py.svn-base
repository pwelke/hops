'''
Created on Apr 20, 2015

@author: irma
'''
import numpy
import os  
import time  
import pickle,math
import copy
from experiments import sampler_general_ex as smplr
from experiments import sampling_utils as su
import experiments.globals
from decimal import Decimal, getcontext

'Standard False Furer reporting at the end of the execution'
def report(output_path,detailed_result_path,fudicts,plot_result_dict,all_furer_times,exhaustive_approach_result_file,data_graph,pattern,Plist,NLIMIT_values,repetitions,pattern_file_name,iteration_counter_n_limit,n_limit_embeddings):
    if (len(fudicts)==0):
        with open(os.path.join(output_path,'no_results.info'), 'wb') as file:
            file.write("No results for random - empty fudicts!")
    
    pickout = open(os.path.join(output_path,'fudicts.pickle'), 'wb')
    pickle.dump(fudicts, pickout)
    pickout.close()
    
    pickout = open(os.path.join(output_path,'all_furer_times.pickle'), 'wb')
    pickle.dump(all_furer_times, pickout)
    pickout.close()
    
    picklename = os.path.join(exhaustive_approach_result_file,"fdict_exhaustive_%s.pickle" % pattern_file_name)
    pickin = open(picklename, 'rb')
    fdict_exhaustive = pickle.load(pickin)
    
    smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
    smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
    
    for nli in range(len(NLIMIT_values)):
        plot_result_dict[NLIMIT_values[nli]] = {}
        furer_results_KLD = []
        furer_results_bhatta = []
        furer_results_hellinger = []
        furer_times = []
        
        for i in range(repetitions):
            furer_times.append(all_furer_times[i][nli])
            fdict_limited = fudicts[i][nli]
            smplr.smooth(fdict_limited,  fdict_exhaustive)    # smoothing to avoid zeros
            fdict_Furer = fudicts[i][nli]   
            
            [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default(fdict_exhaustive,  trash_factor=0.01)     # we remove rows where frequencies do not reach 1%            
            
            if len(pde) < 1:
                print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                break

            [pdl,  tl,  dk] = smplr.make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
            [pdf ,  tl,  dk]= smplr.make_pd_general_kickout_default_limited(fdict_Furer,  trash_list,  default_key)
            
            emb=n_limit_embeddings[nli]
            
            furer_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
            furer_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
            furer_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
              
      
        plot_result_dict[NLIMIT_values[nli]]["furer_KLD"] = (numpy.mean(furer_results_KLD),  numpy.std(furer_results_KLD,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["furer_BHT"] = (numpy.mean(furer_results_bhatta),  numpy.std(furer_results_bhatta,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["furer_HEL"] = (numpy.mean(furer_results_hellinger),  numpy.std(furer_results_hellinger,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["furer_times"] = (numpy.mean(furer_times),  numpy.std(furer_times,  ddof=1))
 
 
        result_file_name = detailed_result_path+"/"+"res_" + pattern_file_name + pattern_file_name+"."+str(repetitions) +"x"+str(NLIMIT_values[nli])+".result"
        print "RESULT FILE NAME!!!",result_file_name
        
        resultfile = open(result_file_name,  'w')
        resultfile.write('False Furer\n')
        resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
        resultfile.write("NLIMIT: " + str(NLIMIT_values[nli]) +"\n")
        resultfile.write("repetitions: " + str(repetitions) +"\n")
        resultfile.write(" " +"\n")
        resultfile.write("average average KLD on false furer: " + str(numpy.mean(furer_results_KLD))  + " with SSTD: " + str(numpy.std(furer_results_KLD,  ddof=1)) +"\n")
        resultfile.write("average average bhatta on false furer: " + str(numpy.mean(furer_results_bhatta))  + " with SSTD: " + str(numpy.std(furer_results_bhatta,  ddof=1)) +"\n")
        resultfile.write("average average hellinger on false furer: " + str(numpy.mean(furer_results_hellinger))  + " with SSTD: " + str(numpy.std(furer_results_hellinger,  ddof=1)) +"\n")
        resultfile.write(" " +"\n")
        resultfile.write("false furer node took per run on average: " +str(numpy.mean(furer_times)) + " seconds." +"\n")
        resultfile.write('-----DETAILED RESULTS-----' +"\n")
        resultfile.write('false_results_KLD :' + str(furer_results_KLD) +"\n")
        resultfile.write('false_results_bhatta :' + str(furer_results_bhatta) +"\n")
        resultfile.write('false_results_hellinger :' + str(furer_results_hellinger) +"\n")
        resultfile.write('false_times :' + str(furer_times) +"\n")
        resultfile.write('Nr embeddings for limit: '+str(emb))
        resultfile.close()
         
    
'This method is used to report results gathered at a specific time points (given in monitoring_marks). There is no plotting'
def report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_result_file,data_graph,pattern,Plist,repetitions,pattern_file_name):
      #CREATE DIRECTORY THAT WILL CONTAINS RESULTS FOR EACH TIME INSTANCE
      
      picklename = os.path.join(exhaustive_approach_result_file,"fdict_exhaustive_%s.pickle" % pattern_file_name)
      pickin = open(picklename, 'rb')
      fdict_exhaustive = pickle.load(pickin)
      
      smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
      smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
     
      dict={}
      
      duration=[]
      nr_iterations=[]
      sum_of_embeddings=[]
      sum_of_squares=[]
      sum_of_root_node_emb=[]
      sum_of_squares_root_node_emb=[]
      begin=0
      
      for time_int in monitoring_marks:
          duration.append(time_int-begin)
          begin=time_int
      
      
      #the problem might be that some runs finished earlier, and some later.
      for i in xrange(len(monitoring_marks)):
          for key_iter in monitoring_reports.keys():
              if not(monitoring_marks[i] in dict.keys()):
                  dict[monitoring_marks[i]]=[]
              try:
                  dict[monitoring_marks[i]].append(monitoring_reports[key_iter][i])
                  nr_iterations.append(monitoring_reports[key_iter][i].nr_iterations)
                  sum_of_embeddings.append(monitoring_reports[key_iter][i].sum_nr_embeddings)
                  sum_of_squares.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings)
                  sum_of_root_node_emb.append(monitoring_reports[key_iter][i].sum_nr_extra_embeddings)
                  sum_of_squares_root_node_emb.append(monitoring_reports[key_iter][i].sum_of_the_extra_square_embeddings)
                  
              except IndexError:
                  break

      print "NR ITERATIONS: ",nr_iterations
      print "sum_of_embeddings: ",sum_of_embeddings
      print "sum_of_squares: ",sum_of_squares
      snapshot_inits=[]
      for i in range(repetitions):
          snapshot_inits.append(0)
      
      counter_duration=0
      counter=0
      for time_snapshot in monitoring_marks:
          false_furer_results_KLD = []
          false_furer_results_bhatta = []
          false_furer_results_hellinger = []
          false_furer_times = []
          observed_nodes=[]
          observed_nodes_difference_per_snapshot=[]
          
          snapshot_directory_path=os.path.join(detailed_result_path,)
          if not(os.path.exists(snapshot_directory_path)):
              os.mkdir(snapshot_directory_path)
          snapshot_directory_file=os.path.join(snapshot_directory_path,'res_time_'+str(time_snapshot)+'.info')
          
          fdict_furer_temp=dict[time_snapshot]
          
          fdicts_Furer=[]
          
          for f in fdict_furer_temp:
              fdicts_Furer.append(f.current_fdict)
              observed_nodes.append(f.number_of_observed_nodes)
          
          if len(fdict_furer_temp)==0:
              continue
          
          for i in range(len(fdict_furer_temp)):
              fdict_limited = fdicts_Furer[i]
              smplr.smooth(fdict_limited,  fdict_exhaustive)    # smoothing to avoid zeros
              fdict_Furer=fdicts_Furer[i]
                
              observed_nodes_difference_per_snapshot.append(observed_nodes[i]-snapshot_inits[i])
              snapshot_inits[i]=observed_nodes[i]
              
              [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default(fdict_exhaustive,  trash_factor=0.01)
             
              if len(pde) < 1:
                  print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                  break
              
              #[pdl,  tl,  dk] = smplr.make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
              [pdf ,  tl,  dk]= smplr.make_pd_general_kickout_default_limited(fdict_Furer,  trash_list,  default_key)
              false_furer_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
              false_furer_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
              false_furer_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
          
          
          print "Writing to: ",snapshot_directory_file
          resultfile = open(snapshot_directory_file,  'w')
          resultfile.write('False Furer\n')
          resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
          resultfile.write("repetitions (for this time snapshot): " + str(repetitions) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write("average KLD on false furer: " + str(numpy.mean(false_furer_results_KLD))  + " with SSTD: " + str(numpy.std(false_furer_results_KLD,  ddof=1)) +"\n")
          resultfile.write("average bhatta on false furer: " + str(numpy.mean(false_furer_results_bhatta))  + " with SSTD: " + str(numpy.std(false_furer_results_bhatta,  ddof=1)) +"\n")
          resultfile.write("average hellinger on false furer: " + str(numpy.mean(false_furer_results_hellinger))  + " with SSTD: " + str(numpy.std(false_furer_results_hellinger,  ddof=1)) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write('-----DETAILED RESULTS-----' +"\n")
          resultfile.write('false_results_KLD :' + str(false_furer_results_KLD) +"\n")
          resultfile.write('false_results_bhatta :' + str(false_furer_results_bhatta) +"\n")
          resultfile.write('false_results_hellinger :' + str(false_furer_results_hellinger) +"\n")
          resultfile.write('avg #nodes observed :' + str(numpy.mean(observed_nodes)) +"\n")
          resultfile.write('# nodes per time interval per run:' + str((numpy.mean(observed_nodes_difference_per_snapshot)/duration[counter_duration])) +"\n")
          resultfile.write('avg difference of nodes observed from previous snapshot :' + str(numpy.mean(observed_nodes_difference_per_snapshot)) +"\n")          
          resultfile.write("------------------------------------ Sampling info ------------------------------\n")
          resultfile.write('number of sampling iterations : ' + str(nr_iterations[counter])+"\n")    
          resultfile.write('average of embeddings : ' + str(sum_of_embeddings[counter]/nr_iterations[counter])+"\n")        
          #resultfile.write('average of embeddings w.r.t sampling iterations:' + str(sum_of_embeddings[counter]/float(nr_iterations[counter]))+"\n") 
          if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
             nr_embeddings_temp=sum_of_embeddings[counter]/nr_iterations[counter]
          else:
             nr_embeddings_temp=sum_of_root_node_emb[counter]/nr_iterations[counter] 
          
          print "Writing to file: ",nr_embeddings_temp
          resultfile.write('average of embeddings : ' + str(nr_embeddings_temp)+"\n")   
          if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
              #we do the old standard deviation
              a=Decimal(sum_of_squares[counter])-(Decimal(math.pow(sum_of_embeddings[counter], 2))/Decimal(float(nr_iterations[counter])))
              stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
          else:
              a=Decimal(sum_of_squares_root_node_emb[counter])-(Decimal(math.pow(sum_of_root_node_emb[counter], 2))/Decimal(float(nr_iterations[counter])))
              stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
          print "old stdev: ",stdeviation
          resultfile.write('stdeviation of # embeddings: ' + str(stdeviation)+"\n") 
          resultfile.close()
          counter+=1
          counter_duration+=1      
          
#           avg=sum_of_embeddings[counter]/float(nr_iterations[counter])
#           getcontext().prec = 3
#           print "AVG: ",avg
#           print "Sum od squares: ",Decimal(sum_of_squares[counter])
#           print "Sum number of embeddings: ",Decimal(sum_of_embeddings[counter])
#           print "Nr iterations: ",nr_iterations[counter]
#           print "A1: ",sum_of_squares[counter]
#           print "A2: ",sum_of_embeddings[counter]*avg
#           
#           print Decimal(sum_of_squares[counter])
#           print Decimal(sum_of_embeddings[counter]*avg)
#           hello= (sum_of_squares[counter]-(sum_of_embeddings[counter]*avg))
#           print hello
#           print "A3: ",long(sum_of_squares[counter]-(sum_of_embeddings[counter]*avg))
#           print "A3 Decimal: ",Decimal(sum_of_squares[counter]) - Decimal(sum_of_embeddings[counter]*avg)
#           print "Other kind of average!",(sum_of_squares[counter]-sum_of_embeddings[counter]*avg)/(nr_iterations[counter]-1)
#           a=float(sum_of_squares[counter])-((math.pow(sum_of_embeddings[counter], 2)/float(nr_iterations[counter])))
#           print "Brojnik: ",a
#           #if a<0:
#           #    stdeviation=0.0
#           #else:
#           stdeviation=math.sqrt(a/(nr_iterations[counter]-1))
#           print "STDEV: ",stdeviation
#           resultfile.write('stdeviation of # embeddings: ' + str(stdeviation)+"\n") 
#           resultfile.close()
#           counter+=1
#           counter_duration+=1    
#           resultfile.close()
def report_monitoring_my_version_online(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_result_file,data_graph,pattern,Plist,repetitions,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations):
      dict={}
      
      duration=[]
      nr_iterations=[]
      sum_of_embeddings=[]
      sum_of_squares=[]
      sum_of_root_node_emb=[]
      sum_of_squares_root_node_emb=[]
      begin=0
      
      for time_int in monitoring_marks:
          duration.append(time_int-begin)
          begin=time_int
      
      
      #the problem might be that some runs finished earlier, and some later.
      
      for i in xrange(len(monitoring_marks)):
              print i
          #for key_iter in monitoring_reports.keys():
              if not(monitoring_marks[i] in dict.keys()):
                  dict[monitoring_marks[i]]=[]
              try:
                  dict[monitoring_marks[i]].append(monitoring_reports[i])
                  nr_iterations.append(monitoring_reports[i].nr_iterations)
                  sum_of_embeddings.append(monitoring_reports[i].sum_nr_embeddings)
                  sum_of_squares.append(monitoring_reports[i].sum_of_the_square_embeddings)
                  sum_of_root_node_emb.append(monitoring_reports[i].sum_nr_extra_embeddings)
                  sum_of_squares_root_node_emb.append(monitoring_reports[i].sum_of_the_extra_square_embeddings)
                  
              except IndexError:
                  break

      print "NR ITERATIONS: ",nr_iterations
      print "sum_of_embeddings: ",sum_of_embeddings
      print "sum_of_squares: ",sum_of_squares
      snapshot_inits=[]
      for i in range(repetitions):
          snapshot_inits.append(0)
      
      counter_duration=0
      counter=0
      
      average_klds=[]
      average_bhattas=[]
      average_hellingers=[]
      std_klds=[]
      std_bhattas=[]
      std_hellingers=[]
      avg_nodes_observed=[]
      nr_nodes_per_time_interval_per_runs=[]
      number_of_sampling_iterations=[]
      average_of_embeddings=[]
      stdevs=[]
      
      for time_snapshot in monitoring_marks:
          print "Processing ",counter,"out of: ",len(monitoring_marks)
          false_furer_results_KLD = []
          false_furer_results_bhatta = []
          false_furer_results_hellinger = []
          false_furer_times = []
          observed_nodes=[]
          observed_nodes_difference_per_snapshot=[]
          
          snapshot_directory_path=os.path.join(detailed_result_path,)
          if not(os.path.exists(snapshot_directory_path)):
              os.mkdir(snapshot_directory_path)
          snapshot_directory_file=os.path.join(snapshot_directory_path,'res_time_'+str(time_snapshot)+'.info')
          
          fdict_furer_temp=dict[time_snapshot]
          
          fdicts_Furer=[]
          
          for f in fdict_furer_temp:
              fdicts_Furer.append(f.current_fdict)
              observed_nodes.append(f.number_of_observed_nodes)
          
          if len(fdict_furer_temp)==0:
              continue
          
          for i in range(len(fdict_furer_temp)):
              experiments.globals.nr_iterations=nr_iterations[i]
              fdict_limited = fdicts_Furer[i]
              fdict_Furer=fdicts_Furer[i]
              observed_nodes_difference_per_snapshot.append(observed_nodes[i]-snapshot_inits[i])
              snapshot_inits[i]=observed_nodes[i]
              
              [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default_my_version(fdict_exhaustive)
             
              if len(pde) < 1:
                  print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                  break
              print fdict_Furer
              nr_possible_combinations=smplr.complete_combinations_1(fdict_Furer, data_graph,  pattern,  Plist)
              pdf= smplr.make_pd_general_kickout_default_limited_my_version(fdict_Furer)
              #print smplr.transform_to_ptable(pde)
              #print smplr.transform_to_ptable(pdf)
              false_furer_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
              false_furer_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
              false_furer_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))

          
          average_klds.append(numpy.mean(false_furer_results_KLD))
          std_klds.append(numpy.std(false_furer_results_KLD,  ddof=1))
          average_bhattas.append(numpy.mean(false_furer_results_bhatta))
          std_bhattas.append(numpy.std(false_furer_results_bhatta,  ddof=1))
          average_hellingers.append(numpy.mean(false_furer_results_hellinger))
          std_hellingers.append(numpy.std(false_furer_results_hellinger,  ddof=1))
          avg_nodes_observed.append(numpy.mean(observed_nodes))
          number_of_sampling_iterations.append(nr_iterations[counter])          
          nr_nodes_per_time_interval_per_runs.append(float((numpy.mean(observed_nodes_difference_per_snapshot)/duration[counter_duration])))
          if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
             nr_embeddings_temp=sum_of_embeddings[counter]/nr_iterations[counter]
          else:
             nr_embeddings_temp=sum_of_root_node_emb[counter]/nr_iterations[counter] 
          average_of_embeddings.append(nr_embeddings_temp)
          stdeviation=numpy.nan
          try:
              if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
                  #we do the old standard deviation
                  a=Decimal(sum_of_squares[counter])-(Decimal(math.pow(sum_of_embeddings[counter], 2))/Decimal(float(nr_iterations[counter])))
                  stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
              else:
                  a=Decimal(sum_of_squares_root_node_emb[counter])-(Decimal(math.pow(sum_of_root_node_emb[counter], 2))/Decimal(float(nr_iterations[counter])))
                  stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
          except:
              print "not successful"
              
          stdevs.append(stdeviation)
          
          
          counter+=1
          counter_duration+=1   
      return {"average_klds":average_klds,"average_bhattas":average_bhattas,"average_hellingers":average_hellingers,"std_klds":std_klds,"std_bhattas":std_bhattas,"std_hellingers":std_hellingers,"avg_nodes_observed":avg_nodes_observed,"nr_nodes_per_time_interval_per_runs":nr_nodes_per_time_interval_per_runs,"number_of_sampling_iterations":number_of_sampling_iterations,"average_of_embeddings":average_of_embeddings,"stdevs":stdevs}
                         
          
          
          
          
def report_monitoring_my_version(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_result_file,data_graph,pattern,Plist,repetitions,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations,write):
      #CREATE DIRECTORY THAT WILL CONTAINS RESULTS FOR EACH TIME INSTANCE
      
      #picklename = os.path.join(exhaustive_approach_result_file,"fdict_exhaustive_%s.pickle" % pattern_file_name)
      #pickin = open(picklename, 'rb')
      #fdict_exhaustive = pickle.load(pickin)
      
      #smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
      #smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
     
      dict={}
      
      duration=[]
      nr_iterations=[]
      sum_of_embeddings=[]
      sum_of_squares=[]
      sum_of_root_node_emb=[]
      sum_of_squares_root_node_emb=[]
      begin=0
      
      for time_int in monitoring_marks:
          duration.append(time_int-begin)
          begin=time_int
      
      
      #the problem might be that some runs finished earlier, and some later.
      for i in xrange(len(monitoring_marks)):
          for key_iter in monitoring_reports.keys():
              if not(monitoring_marks[i] in dict.keys()):
                  dict[monitoring_marks[i]]=[]
              try:
                  dict[monitoring_marks[i]].append(monitoring_reports[key_iter][i])
                  nr_iterations.append(monitoring_reports[key_iter][i].nr_iterations)
                  sum_of_embeddings.append(monitoring_reports[key_iter][i].sum_nr_embeddings)
                  sum_of_squares.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings)
                  sum_of_root_node_emb.append(monitoring_reports[key_iter][i].sum_nr_extra_embeddings)
                  sum_of_squares_root_node_emb.append(monitoring_reports[key_iter][i].sum_of_the_extra_square_embeddings)
                  
              except IndexError:
                  break

      print "NR ITERATIONS: ",nr_iterations
      print "sum_of_embeddings: ",sum_of_embeddings
      print "sum_of_squares: ",sum_of_squares
      snapshot_inits=[]
      for i in range(repetitions):
          snapshot_inits.append(0)
      
      counter_duration=0
      counter=0
      for time_snapshot in monitoring_marks:
          print "Processing ",counter,"out of: ",len(monitoring_marks)
          false_furer_results_KLD = []
          false_furer_results_bhatta = []
          false_furer_results_hellinger = []
          false_furer_times = []
          observed_nodes=[]
          observed_nodes_difference_per_snapshot=[]
          
          snapshot_directory_path=os.path.join(detailed_result_path,)
          if not(os.path.exists(snapshot_directory_path)):
              os.mkdir(snapshot_directory_path)
          snapshot_directory_file=os.path.join(snapshot_directory_path,'res_time_'+str(time_snapshot)+'.info')
          
          if write==True:
              fdict_furer_temp=dict[time_snapshot]
              
              fdicts_Furer=[]
              
              for f in fdict_furer_temp:
                  fdicts_Furer.append(f.current_fdict)
                  observed_nodes.append(f.number_of_observed_nodes)
              
              if len(fdict_furer_temp)==0:
                  continue
              
              for i in range(len(fdict_furer_temp)):
                  experiments.globals.nr_iterations=nr_iterations[i]
                  fdict_limited = fdicts_Furer[i]
                  fdict_Furer=fdicts_Furer[i]
                  observed_nodes_difference_per_snapshot.append(observed_nodes[i]-snapshot_inits[i])
                  snapshot_inits[i]=observed_nodes[i]
                  
                  [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default_my_version(fdict_exhaustive)
                 
                  if len(pde) < 1:
                      print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                      break
                  nr_possible_combinations=smplr.complete_combinations_1(fdict_Furer, data_graph,  pattern,  Plist)
                  pdf= smplr.make_pd_general_kickout_default_limited_my_version(fdict_Furer)
                  false_furer_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
                  false_furer_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
                  false_furer_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdf)))
          
          
          print "Writing to: ",snapshot_directory_file
          resultfile = open(snapshot_directory_file,  'w')
          resultfile.write('False Furer\n')
          resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
          resultfile.write("repetitions (for this time snapshot): " + str(repetitions) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write("average KLD on false furer: " + str(numpy.mean(false_furer_results_KLD))  + " with SSTD: " + str(numpy.std(false_furer_results_KLD,  ddof=1)) +"\n")
          resultfile.write("average bhatta on false furer: " + str(numpy.mean(false_furer_results_bhatta))  + " with SSTD: " + str(numpy.std(false_furer_results_bhatta,  ddof=1)) +"\n")
          resultfile.write("average hellinger on false furer: " + str(numpy.mean(false_furer_results_hellinger))  + " with SSTD: " + str(numpy.std(false_furer_results_hellinger,  ddof=1)) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write('-----DETAILED RESULTS-----' +"\n")
          resultfile.write('false_results_KLD :' + str(false_furer_results_KLD) +"\n")
          resultfile.write('false_results_bhatta :' + str(false_furer_results_bhatta) +"\n")
          resultfile.write('false_results_hellinger :' + str(false_furer_results_hellinger) +"\n")
          resultfile.write('avg #nodes observed :' + str(numpy.mean(observed_nodes)) +"\n")
          resultfile.write('# nodes per time interval per run:' + str((numpy.mean(observed_nodes_difference_per_snapshot)/duration[counter_duration])) +"\n")
          resultfile.write('avg difference of nodes observed from previous snapshot :' + str(numpy.mean(observed_nodes_difference_per_snapshot)) +"\n")          
          resultfile.write("------------------------------------ Sampling info ------------------------------\n")
          resultfile.write('number of sampling iterations : ' + str(nr_iterations[counter])+"\n")    
          #resultfile.write('average of embeddings : ' + str(sum_of_embeddings[counter]/nr_iterations[counter])+"\n")        
          #resultfile.write('average of embeddings w.r.t sampling iterations:' + str(sum_of_embeddings[counter]/float(nr_iterations[counter]))+"\n") 
          if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
             nr_embeddings_temp=sum_of_embeddings[counter]/nr_iterations[counter]
          else:
             nr_embeddings_temp=sum_of_root_node_emb[counter]/nr_iterations[counter] 
          
          print "Writing to file: ",nr_embeddings_temp
          resultfile.write('average of embeddings : ' + str(nr_embeddings_temp)+"\n")   
          if sum_of_squares_root_node_emb[counter]==0 and sum_of_root_node_emb[counter]==0:
              #we do the old standard deviation
              a=Decimal(sum_of_squares[counter])-(Decimal(math.pow(sum_of_embeddings[counter], 2))/Decimal(float(nr_iterations[counter])))
              if a>0:
                stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
              else:
                  stdeviation=0
              
          else:
              a=Decimal(sum_of_squares_root_node_emb[counter])-(Decimal(math.pow(sum_of_root_node_emb[counter], 2))/Decimal(float(nr_iterations[counter])))
              if a>0:
                stdeviation=math.sqrt(a/Decimal(float((nr_iterations[counter]-1))))
              else:
                stdeviation=0
          print "old stdev: ",stdeviation
          resultfile.write('stdeviation of # embeddings: ' + str(stdeviation)+"\n") 
          resultfile.close()
          counter+=1
          counter_duration+=1   
               