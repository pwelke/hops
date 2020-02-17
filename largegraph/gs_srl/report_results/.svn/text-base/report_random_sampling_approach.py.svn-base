'''
Created on Apr 17, 2015

@author: irma
'''
import numpy,math
import os  
import time  
import pickle
import copy
import experiments.globals
from experiments import sampler_general_ex as smplr
from experiments import sampling_utils as su
from decimal import Decimal, getcontext


    
def report(rndicts,all_randnode_times,NLIMIT_values,plot_result_dict,repetitions,detailed_result_path,output_path,exhaustive_approach_result_file,pattern_file_name,nr_embeddings_n_limits):
    if (len(rndicts)==0):
        with open(os.path.join(output_path,'no_results.info'), 'wb') as file:
            file.write("No results for random - empty rndicts!")
            
    
    pickout = open(os.path.join(output_path,'rndicts.pickle'), 'wb')
    pickle.dump(rndicts, pickout)
    pickout.close()
      
    pickout = open(os.path.join(output_path,'all_randnode_times.pickle'), 'wb')
    pickle.dump(all_randnode_times, pickout)
    pickout.close()
      
    picklename = os.path.join(exhaustive_approach_result_file,"fdict_exhaustive_%s.pickle" % pattern_file_name)
    pickin = open(picklename, 'rb')
    fdict_exhaustive = pickle.load(pickin)
  
    for nli in range(len(NLIMIT_values)):
        plot_result_dict[NLIMIT_values[nli]] = {}
        randnode_results_KLD = []
        randnode_results_bhatta = []
        randnode_results_hellinger = []
        randnode_times = []
         
        for i in range(repetitions):
            emb=nr_embeddings_n_limits[nli]
            randnode_times.append(all_randnode_times[i][nli])
            fdict_limited = rndicts[i][nli]
            smplr.smooth(fdict_limited,  fdict_exhaustive)    # smoothing to avoid zeros    
            [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default(fdict_exhaustive,  trash_factor=0.01)     # we remove rows where frequencies do not reach 1%            
            if len(pde) < 1:
                print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                break
            #print "pde length: ",len(pde)
            [pdl,  tl,  dk] = smplr.make_pd_general_kickout_default_limited(fdict_limited,  trash_list,  default_key)
            #print "fdict exhaustive: ",len(fdict_exhaustive),"fdict limited",len(fdict_limited)
            # new function also for limited ones : make_pd_general_kickout_default_limited(fdict,  trash,  default_key)          
            randnode_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
            randnode_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
            randnode_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
              
        plot_result_dict[NLIMIT_values[nli]]["randomnode_KLD"] = (numpy.mean(randnode_results_KLD),  numpy.std(randnode_results_KLD,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["randomnode_BHT"] = (numpy.mean(randnode_results_bhatta),  numpy.std(randnode_results_bhatta,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["randomnode_HEL"] = (numpy.mean(randnode_results_hellinger),  numpy.std(randnode_results_hellinger,  ddof=1))
     
    # added to store and plot the times
        plot_result_dict[NLIMIT_values[nli]]["randomnode_times"] = (numpy.mean(randnode_times),  numpy.std(randnode_times,  ddof=1))
        plot_result_dict[NLIMIT_values[nli]]["randomnode_times"] = (numpy.mean(randnode_times),  numpy.std(randnode_times,  ddof=1))
 
        result_file_name = detailed_result_path+"/"+"ultimex_ICDM_" + pattern_file_name + pattern_file_name+"."+str(repetitions) +"x"+str(NLIMIT_values[nli])+".result"
        print "RESULT FILE NAME: ",result_file_name
        resultfile = open(result_file_name,  'w')
        resultfile.write('Random Vertex\n')
        resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
        resultfile.write("NLIMIT: " + str(NLIMIT_values[nli]) +"\n")
        resultfile.write("repetitions: " + str(repetitions) +"\n")
        resultfile.write(" " +"\n")
        resultfile.write("average average KLD on randomnode: " + str(numpy.mean(randnode_results_KLD))  + " with SSTD: " + str(numpy.std(randnode_results_KLD,  ddof=1)) +"\n")
        resultfile.write("average average bhatta on randomnode: " + str(numpy.mean(randnode_results_bhatta))  + " with SSTD: " + str(numpy.std(randnode_results_bhatta,  ddof=1)) +"\n")
        resultfile.write("average average hellinger on randomnode: " + str(numpy.mean(randnode_results_hellinger))  + " with SSTD: " + str(numpy.std(randnode_results_hellinger,  ddof=1)) +"\n")
        resultfile.write(" " +"\n")
        resultfile.write("Random node took per run on average: " +str(numpy.mean(randnode_times)) + " seconds." +"\n")
        resultfile.write('-----DETAILED RESULTS-----' +"\n")
        resultfile.write('randnode_results_KLD :' + str(randnode_results_KLD) +"\n")
        resultfile.write('randnode_results_bhatta :' + str(randnode_results_bhatta) +"\n")
        resultfile.write('randnode_results_hellinger :' + str(randnode_results_hellinger) +"\n")
        resultfile.write('randnode_times :' + str(randnode_times) +"\n")
        resultfile.write('Nr embeddings for limit: '+str(emb))
        resultfile.close()
        
        
def report_monitoring_my_version(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_result_file,data_graph,pattern,Plist,repetitions,pattern_file_name,fdict_exhaustive,nr_non_observed_combinations,write):
      #CREATE DIRECTORY THAT WILL CONTAINS RESULTS FOR EACH TIME INSTANCE
      dict={}
      duration=[]
      nr_iterations=[]
      sum_number_of_embeddings=[]
      sum_of_embeddings_vers1=[]
      sum_of_embeddings_random_old=[]
      sum_of_square_emb_random_old=[]
      
      sum_of_squares_vers1=[]
      sum_of_the_square_embeddings=[]
      nr_root_nodes=[]
      begin=0
      
      for time_int in monitoring_marks:
          duration.append(time_int-begin)
          begin=time_int
      
      #if not type(monitoring_reports)==dict:
      #  print "monitoring reports to dictionary"
      #  tmp=monitoring_reports
      #  monitoring_reports={}
      #  monitoring_reports["1"]=tmp
      #  print monitoring_reports
      #the problem might be that some runs finished earlier, and some later.
      for i in xrange(len(monitoring_marks)):
          for key_iter in monitoring_reports.keys():
              if not(monitoring_marks[i] in dict.keys()):
                  dict[monitoring_marks[i]]=[]
              try:
                  dict[monitoring_marks[i]].append(monitoring_reports[key_iter][i])
                  nr_iterations.append(monitoring_reports[key_iter][i].nr_iterations)
                  sum_number_of_embeddings.append(monitoring_reports[key_iter][i].sum_nr_embeddings)
                  sum_of_the_square_embeddings.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings)
                  nr_root_nodes.append(monitoring_reports[key_iter][i].nr_root_nodes)
                  try:
                      sum_of_embeddings_random_old.append(monitoring_reports[key_iter][i].sum_number_of_embeddings_random)
                      sum_of_square_emb_random_old.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings_random)
                  except:
                      continue  
                  try:
                      sum_of_embeddings_vers1.append(monitoring_reports[key_iter][i].sum_nr_embeddings_aux)
                      sum_of_squares_vers1.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings_aux)
                  except:
                      continue
                  
              except IndexError:
                  break
      print "Sum of embeddings random old: ",len(sum_of_embeddings_random_old)
      print "NR ITERATIONS: ",nr_iterations
      print "sum_of_embeddings: ",sum_of_embeddings_vers1
      print "sum_of_squares: ",sum_of_squares_vers1
      snapshot_inits=[]
      for i in range(repetitions):
          snapshot_inits.append(0)
      
      counter_duration=0
      counter=0
      interval=0
      acc_nr_emb=0
      acc_nr_emb_minus_average=0
      nr_emb_per_interval=[]
      
      for time_snapshot in monitoring_marks:
          experiments.globals.current_time_snapshot=time_snapshot
          print "TIME SNAPSHOT: ",time_snapshot
          interval+=1
          randnode_results_KLD = []
          randnode_results_bhatta = []
          randnode_results_hellinger = []          
          furer_times = []
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
                  
                  [pde,  trash_list,default_key] = smplr.make_pd_general_kickout_default_my_version(fdict_exhaustive)
                  if len(pde) < 1:
                      print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                      break  
                 
                  #if time_snapshot==15:
                  #    for ke in pde.keys():
                  #        print ke,pde[ke]
                  
                  nr_possible_combinations=smplr.complete_combinations_1(fdict_Furer, data_graph,  pattern,  Plist)
                  
                  pdl= smplr.make_pd_general_kickout_default_limited_my_version(fdict_Furer)
    #               print "EXHAUSTIVE:"
    #               for k in pde.keys():
    #                     print "KEY: ",k
    #                     for e in pde[k]:
    #                         print e
    #               print "SMPL:"
    #               for k in pdl.keys():
    #                     print "KEY: ",k
    #                     for e in pdl[k]:
    #                         print e
                  #print "EXHAUSTIVE ..."
                  #with open('random_exhaustive.csv','w') as f:
                  #   for k in pde.keys():
                  #      print "KEY: ",k
                  #      f.write(str(k)+";")
                  #      for e in pde[k]:
                  #          f.write(str(e)+";")
                  #      f.write("\n")
                  #print "RANDOM ..."
                  #with open('random_random.csv','w') as f:
                  #   for k in pdl.keys():
                  #      f.write(str(k)+";")
                  #      for e in pdl[k]:
                  #          f.write(str(e)+";")
                  #      f.write("\n")
                  randnode_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
                  randnode_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
                  randnode_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
          
          print randnode_results_KLD
          print "Writing to: ",snapshot_directory_file
          resultfile = open(snapshot_directory_file,  'w')
          resultfile.write('Random\n')
          resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
          resultfile.write("repetitions (for this time snapshot): " + str(repetitions) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write("average KLD on random: " + str(numpy.mean(randnode_results_KLD))  + " with SSTD: " + str(numpy.std(randnode_results_KLD,  ddof=1)) +"\n")
          print "KLD: ",str(numpy.mean(randnode_results_KLD))
          resultfile.write("average bhatta on random: " + str(numpy.mean(randnode_results_bhatta))  + " with SSTD: " + str(numpy.std(randnode_results_bhatta,  ddof=1)) +"\n")
          resultfile.write("average hellinger on random: " + str(numpy.mean(randnode_results_hellinger))  + " with SSTD: " + str(numpy.std(randnode_results_hellinger,  ddof=1)) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write('-----DETAILED RESULTS-----' +"\n")
          resultfile.write('random_results_KLD :' + str(randnode_results_KLD) +"\n")
          resultfile.write('random_results_bhatta :' + str(randnode_results_bhatta) +"\n")
          resultfile.write('random_results_hellinger :' + str(randnode_results_hellinger) +"\n")
          resultfile.write('avg #nodes observed :' + str(numpy.mean(observed_nodes)) +"\n")
          resultfile.write('# nodes per time interval per run:' + str((numpy.mean(observed_nodes_difference_per_snapshot)/duration[counter_duration])) +"\n")
          resultfile.write('avg difference of nodes observed from previous snapshot :' + str(numpy.mean(observed_nodes_difference_per_snapshot)) +"\n")          
          resultfile.write("------------------------------------ Sampling info ------------------------------\n")
          resultfile.write('number of sampling iterations :' + str(nr_iterations[counter])+"\n")    
          nr_iter=nr_iterations[counter]
          if nr_iter==0 or nr_iter==1:
              nr_iter=2
          avg=(float(Decimal(sum_number_of_embeddings[counter]))/nr_iter)*(experiments.globals.nr_root_nodes)
          print "HALOOO:", Decimal(sum_number_of_embeddings[counter])
          old=False
          stdev2=0
          if avg<0:
              print "Handling old data structures"
              #this means we handle the old version
              avg=float(sum_of_embeddings_random_old[counter])/nr_iter
              old=True
          sum1=Decimal(sum_of_the_square_embeddings[counter])
          sum2=Decimal(sum_number_of_embeddings[counter])
          var=Decimal(sum1)-(Decimal(math.pow(Decimal(sum2),2))/nr_iter)
          print "Variance: ",var
          if var>0:
            stdev2=math.sqrt(var/(nr_iter-1))
       
          stdev=Decimal(stdev2)*Decimal(math.sqrt(nr_iter)) 
          if old:
              print "Handling old data structures"
              #this means we handle the old version
              variance=sum_of_square_emb_random_old[counter]/(nr_iter)
              stdev2=math.sqrt(variance/(nr_iter-1))
          print "STDEV: ",stdev
          print "STDEV 2: ",stdev2
          print "Nr embeddingS: ",avg
          resultfile.write('average of embeddings w.r.t sampling iterations:' +str(avg) +"\n") 
          resultfile.write('stdeviation of # embeddings:' + str(stdev2)+"\n")  
          resultfile.write('2 stdeviation of # embeddings:' + str(stdev)+"\n")  
          counter+=1  
          resultfile.close()
          counter_duration+=1
        
        
        
'This method is used to report results gathered at a specific time points (given in monitoring_marks). There is no plotting'
def report_monitoring(monitoring_marks,output_path,detailed_result_path,monitoring_reports,exhaustive_approach_result_file,data_graph,pattern,Plist,repetitions,pattern_file_name):
      #CREATE DIRECTORY THAT WILL CONTAINS RESULTS FOR EACH TIME INSTANCE
      picklename = os.path.join(exhaustive_approach_result_file,"fdict_exhaustive_%s.pickle" % pattern_file_name)
      pickin = open(picklename, 'rb')
      fdict_exhaustive = pickle.load(pickin)
      #smplr.complete_combinations(fdict_exhaustive, data_graph,  pattern,  Plist)      # add zeros to all not present combinations
      #smplr.smooth(fdict_exhaustive,  fdict_exhaustive)     # Laplace smoothing also for the exhaustive
      dict={}
      duration=[]
      nr_iterations=[]
      sum_number_of_embeddings=[]
      sum_of_embeddings_vers1=[]
      sum_of_squares_vers1=[]
      sum_of_the_square_embeddings=[]
      sum_of_embeddings_random_old=[]
      sum_of_square_emb_random_old=[]
      nr_root_nodes=[]
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
                  sum_number_of_embeddings.append(monitoring_reports[key_iter][i].sum_nr_embeddings)
                  sum_of_the_square_embeddings.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings)
                  nr_root_nodes.append(monitoring_reports[key_iter][i].nr_root_nodes)
                  try:
                      sum_of_embeddings_random_old.append(monitoring_reports[key_iter][i].sum_number_of_embeddings_random)
                      sum_of_square_emb_random_old.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings_random)
                  except:
                      continue  
                  try:
                      sum_of_embeddings_vers1.append(monitoring_reports[key_iter][i].sum_nr_embeddings_aux)
                      sum_of_squares_vers1.append(monitoring_reports[key_iter][i].sum_of_the_square_embeddings_aux)
                  except:
                      continue
                       
              except IndexError:
                  break
      
      print "NR ITERATIONS: ",nr_iterations
      print "sum_of_embeddings: ",sum_of_embeddings_vers1
      print "sum_of_squares: ",sum_of_squares_vers1
      snapshot_inits=[]
      for i in range(repetitions):
          snapshot_inits.append(0)
      
      counter_duration=0
      counter=0
      interval=0
      acc_nr_emb=0
      acc_nr_emb_minus_average=0
      nr_emb_per_interval=[]
      
      for time_snapshot in monitoring_marks:
          interval+=1
          randnode_results_KLD = []
          randnode_results_bhatta = []
          randnode_results_hellinger = []          
          furer_times = []
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
              [pde,  trash_list,  default_key] = smplr.make_pd_general_kickout_default_old(fdict_exhaustive,  trash_factor=0.01)
              if len(pde) < 1:
                  print "WARNING: bad (not enough present) pattern or too high trash threshold! STOPPING."
                  break   
              print "random vertex counts: "
              #for k in fdict_limited.keys():
              #    print k,fdict_limited[k]
              [pdl,  tl,  dk] = smplr.make_pd_general_kickout_default_limited_old(fdict_limited,  trash_list,  default_key)
              randnode_results_KLD.append(su.avg_kld(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
              randnode_results_bhatta.append(su.avg_bhatta(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
              randnode_results_hellinger.append(su.avg_hellinger(smplr.transform_to_ptable(pde), smplr.transform_to_ptable(pdl)))
          
          
          print "Writing to: ",snapshot_directory_file
          resultfile = open(snapshot_directory_file,  'w')
          resultfile.write('Random\n')
          resultfile.write("experiment on graph: " + str(pattern_file_name) +" and pattern: "+pattern_file_name+"\n")
          resultfile.write("repetitions (for this time snapshot): " + str(repetitions) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write("average KLD on random: " + str(numpy.mean(randnode_results_KLD))  + " with SSTD: " + str(numpy.std(randnode_results_KLD,  ddof=1)) +"\n")
          print "KLD: ",str(numpy.mean(randnode_results_KLD))
          resultfile.write("average bhatta on random: " + str(numpy.mean(randnode_results_bhatta))  + " with SSTD: " + str(numpy.std(randnode_results_bhatta,  ddof=1)) +"\n")
          resultfile.write("average hellinger on random: " + str(numpy.mean(randnode_results_hellinger))  + " with SSTD: " + str(numpy.std(randnode_results_hellinger,  ddof=1)) +"\n")
          resultfile.write(" " +"\n")
          resultfile.write('-----DETAILED RESULTS-----' +"\n")
          resultfile.write('random_results_KLD :' + str(randnode_results_KLD) +"\n")
          resultfile.write('random_results_bhatta :' + str(randnode_results_bhatta) +"\n")
          resultfile.write('random_results_hellinger :' + str(randnode_results_hellinger) +"\n")
          resultfile.write('avg #nodes observed :' + str(numpy.mean(observed_nodes)) +"\n")
          resultfile.write('# nodes per time interval per run:' + str((numpy.mean(observed_nodes_difference_per_snapshot)/duration[counter_duration])) +"\n")
          resultfile.write('avg difference of nodes observed from previous snapshot :' + str(numpy.mean(observed_nodes_difference_per_snapshot)) +"\n")          
          resultfile.write("------------------------------------ Sampling info ------------------------------\n")
          resultfile.write('number of sampling iterations :' + str(nr_iterations[counter])+"\n")    
          
          avg=(float(Decimal(sum_number_of_embeddings[counter]))/nr_iterations[counter])*(experiments.globals.nr_root_nodes)
          print "HALOOO:", Decimal(sum_number_of_embeddings[counter])
          old=False

          if avg<0:
              print "Handling old data structures"
              #this means we handle the old version
              avg=float(sum_of_embeddings_random_old[counter])/nr_iterations[counter]
              old=True
              
          #nr_emb_per_interval.append(avg)
          #print "Nr emb per interval: ",nr_emb_per_interval
          #resultfile.write('average of embeddings w.r.t sampling iterations:' + str(avg)+"\n") 
          #print "Avg old method: ",avg
          #acc_nr_emb+=Decimal(avg)
          #print "Interval: ",interval," Accnr emg: ",acc_nr_emb
          #avg_emb_Jan=acc_nr_emb/(interval)
          #acc_nr_emb_minus_average=0
          #for i in xrange(0,interval):
          #    acc_nr_emb_minus_average+=math.pow((Decimal(nr_emb_per_interval[i])-Decimal(avg_emb_Jan)),2)
          #std_Jan=math.sqrt(acc_nr_emb_minus_average)/(interval)
          #print "STDEV Jan: ",std_Jan
          #print "Average Nr emb: Jan Method: ",avg_emb_Jan
          
          sum1=Decimal(sum_of_the_square_embeddings[counter])
          sum2=Decimal(sum_number_of_embeddings[counter])
          
          #variance=(Decimal(sum1)-Decimal(sum2))/(nr_iterations[counter]-1)
          print "sum 1: ",sum1
          print "sum 2: ",sum2
          #print "Variance: ",variance
          #stdev1=math.sqrt(variance)
          
          var=Decimal(sum1)-(Decimal(math.pow(Decimal(sum2),2))/nr_iterations[counter])
          stdev2=math.sqrt(var/(nr_iterations[counter]-1))
          
          stdev=Decimal(stdev2)*Decimal(math.sqrt(nr_iterations[counter])) 
          if old:
              print "Handling old data structures"
              #this means we handle the old version
              variance=sum_of_square_emb_random_old[counter]/(nr_iterations[counter])
              stdev2=math.sqrt(variance/(nr_iterations[counter]-1))
          print "STDEV: ",stdev
          print "STDEV 2: ",stdev2
          print "Nr embeddingS: ",avg
          resultfile.write('average of embeddings w.r.t sampling iterations:' +str(avg) +"\n") 
          resultfile.write('stdeviation of # embeddings:' + str(stdev2)+"\n")  
          resultfile.write('2 stdeviation of # embeddings:' + str(stdev)+"\n")  
          #resultfile.write('overal nr. of embeddings:' + str(sum_of_embeddings[counter])+"\n") 
          #a=sum_of_squares[counter]-((math.pow(sum_of_embeddings[counter], 2)/nr_iterations[counter]))
          #stdeviation=math.sqrt(a/(nr_iterations[counter]-1))
          #a1=sum_of_squares_vers1[counter]-((math.pow(sum_of_embeddings_vers1[counter], 2)/nr_iterations[counter]))
          #stdeviation1=math.sqrt(a1/(nr_iterations[counter]-1))
          #resultfile.write('stdeviation of # embeddings:' + str(stdeviation)+"\n")  
          
          counter+=1  

          resultfile.close()
          counter_duration+=1
