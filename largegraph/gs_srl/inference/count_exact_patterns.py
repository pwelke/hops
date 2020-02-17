from algorithms import exhaustive_approach
import csv
import time

from algorithms import exhaustive_approach
from inference import ground_target_predicate as gtp


def exact_counting(pattern,data_graph,OBdecomp,root_node,max_time):
    emb=exhaustive_approach.get_nr_embeddings(data_graph, pattern, OBdecomp, root_node, max_time)
    return emb

def exact_counting_no_time_limit(pattern,data_graph,OBdecomp,root_node):
    emb=exhaustive_approach.get_nr_embeddings_no_time_limit(data_graph, pattern, OBdecomp, root_node)
    return emb

def generate_monitoring_marks(time_interval_in_seconds,max_time_in_seconds):
    counter=0
    marks=[]
    while counter+time_interval_in_seconds<=max_time_in_seconds:
        marks.append(counter+time_interval_in_seconds)
        counter=counter+time_interval_in_seconds
    return marks

def satisfied_equivalences(grounding,equivalences):
    if equivalences==None:
        return True
    for eq in equivalences:
        if grounding[eq[0]][1]!=grounding[eq[1]][1]:
            return False
    return True

def satisfied_non_equivalence(grounding,non_equivalences):
    if non_equivalences==None:
        return True
    for eq in non_equivalences:
        if grounding[eq[0]][1]==grounding[eq[1]][1]:
            return False
    return True


def count_combinations_arity_2(grounding_dictionary,ind1,ind2,pattern_equivalences,non_equivalences):
   output_dict={}
   for k in grounding_dictionary.keys():
       #check first if equivalences hold
       if not (satisfied_equivalences(k,pattern_equivalences) and satisfied_non_equivalence(k,non_equivalences)):
           continue
       key=(k[ind1][1],k[ind2][1])
       if not key in output_dict:
           output_dict[key]=grounding_dictionary[k]
       else:
           output_dict[key]+=grounding_dictionary[k]
   #for k in output_dict:
   #    print k,output_dict[k]
   return output_dict

def ground_the_pattern(data_graph,pattern,OBD,root_node,binding_indices,max_time,pattern_equivalences, non_equivalences):
    Plist = [item for sublist in OBD for item in sublist]
    indices=[]
    for b in binding_indices:
        indices.append(Plist.index(b))
    if pattern_equivalences==None:
        patt_equiv_indices=None
    else:
        patt_equiv_indices = []
        for eq in pattern_equivalences:
            ar=[]
            for eq1 in eq:
                ar.append(Plist.index(eq1))
            patt_equiv_indices.append(ar)

    if non_equivalences==None:
        patt_non_equiv_indices=None
    else:
        patt_non_equiv_indices = []
        for eq in non_equivalences:
            ar=[]
            for eq1 in eq:
                ar.append(Plist.index(eq1))
                patt_non_equiv_indices.append(ar)

    dictionary = exact_counting(pattern, data_graph, OBD, root_node,max_time)
    return count_combinations_arity_2(dictionary, indices[0], indices[1],patt_equiv_indices,patt_non_equiv_indices)


def ground_the_target(data_graph,target,OBD,root_node,binding_indices):
    Plist = [item for sublist in OBD for item in sublist]
    indices=[]
    for b in binding_indices:
        indices.append(Plist.index(b))
    dictionary = exact_counting_no_time_limit(target, data_graph, OBD, root_node)
    return count_combinations_arity_2(dictionary, indices[0], indices[1],None,None)

def generate_csv_exact_counts(data_graph,target_graph,target_constant,target_attr,OBDTarget,root_node_target,patterns,OBDPatterns,indices,root_nodes_patterns,pattern_equivalences,non_equivalence,csvfile,fieldnames,time_dict_csv,max_time_exh):
    tg = gtp.find_all_groundings_of_predicates(data_graph, target_attr, target_constant)
    #for each ground target, ground all patterns and perfom counting, output a csv row
    dictionary_target_counts={}
    pattern_groundings=[]

    #count the patterns
    time_dict={}
    counter=0
    for pattern, OBD, root_node, indices in zip(patterns, OBDPatterns, root_nodes_patterns, indices):
        start = time.time()
        pattern_groundings.append(ground_the_pattern(data_graph,pattern,OBD,root_node,indices,max_time_exh,pattern_equivalences[counter],non_equivalence[counter]))
        end = time.time()
        time_dict[pattern]=end - start
        counter += 1
    target_counts=ground_the_target(data_graph, target_graph, OBDTarget, root_node_target, [1,2])

    for target in tg:
        key = (target.node[1]['value'], target.node[2]['value'])
        if key in target_counts:
            nr_target=target_counts[key]
        else:
            nr_target=0
        dictionary_target_counts[key] = nr_target
    #for k in pattern_groundings[0]:
    #    print k,pattern_groundings[0][k]
    with open(csvfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for target in tg:
            res_dict={}
            key = (target.node[1]['value'], target.node[2]['value'])
            res_dict['target']=dictionary_target_counts[key]
            res_dict['dummy']=key
            field_counter=2
            pattern_counter=0
            for p in patterns:
                if key in pattern_groundings[pattern_counter]:
                    res_dict[fieldnames[field_counter]]=pattern_groundings[pattern_counter][key]
                else:
                    res_dict[fieldnames[field_counter]]=0
                field_counter+=1
                pattern_counter+=1
            writer.writerow(res_dict)

    #report times (in seconds) for inference the patterns
    field_time_dict = ['pattern', 'time']
    with open(time_dict_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_time_dict)
        writer.writeheader()
        res={}
        for p in time_dict:
            res['pattern']=p
            res['time']=time_dict[p]
            writer.writerow(res)

