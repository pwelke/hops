import networkx as nx


def parse_line(line):
   out=line.split('(')
   predicate_name=out[0].lstrip().rstrip()
   arguments=out[1].split(',')
   arg1=arguments[0].replace(".","").rstrip().lstrip()
   arg2=arguments[1].replace(".","").replace(")","").lstrip().rstrip()
   return predicate_name,arg1,arg2
def parse_db_yeast(file_name):
    enzyme_dict={}
    function_dict={}
    phenotype_dict={}
    complex_dict={}
    protein_set=[]
    protein_to_node_dict={}
    interaction_dict={}
    location_dict={}
    protein_class={}
    D=nx.Graph()

    with open(file_name,'r') as f:
        for line in f:
            predicate_name, arg1, arg2=parse_line(line)
            if predicate_name=='complex':
                if arg1 in complex_dict:
                    complex_dict[arg1].append(arg2)
                else:
                    complex_dict[arg1] = [arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='enzyme':
                if arg1 in enzyme_dict:
                    enzyme_dict[arg1].append(arg2)
                else:
                    enzyme_dict[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='function':
                if arg1 in function_dict:
                    function_dict[arg1].append(arg2)
                else:
                    function_dict[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='protein_class':
                if arg1 in protein_class:
                    protein_class[arg1].append(arg2)
                else:
                    protein_class[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='location':
                if arg1 in location_dict:
                    location_dict[arg1].append(arg2)
                else:
                    location_dict[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='phenotype':
                if arg1 in phenotype_dict:
                    phenotype_dict[arg1].append(arg2)
                else:
                    phenotype_dict[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)

            if predicate_name=='interaction':
                if arg1 in interaction_dict:
                   if not (arg2 in interaction_dict and arg1 in interaction_dict[arg2]):
                     interaction_dict[arg1].append(arg2)
                else:
                    interaction_dict[arg1]=[arg2]
                if not arg1 in protein_set:
                    protein_set.append(arg1)
                if not arg2 in protein_set:
                        protein_set.append(arg2)
    id=1
    for p in protein_set:
        D.add_node(id,predicate='constant',label='constant: '+p,value=p,name=p,id=id)
        protein_to_node_dict[p]=id
        id=id+1

    for key, value in enzyme_dict.iteritems():
        neigh=protein_to_node_dict[key]
        for v in value:
            D.add_node(id, predicate='enzyme', label='enzyme: ' + v, value=v,name=v,id=id)
            D.add_edge(id,neigh)
            D.add_edge(neigh,id)
            id=id+1

    for key, value in function_dict.iteritems():
        neigh=protein_to_node_dict[key]
        for v in value:
            D.add_node(id, predicate='function', label='function: ' + v, value=v,name=v,id=id)
            D.add_edge(id,neigh)
            D.add_edge(neigh,id)
            id=id+1

    for key, value in location_dict.iteritems():
        neigh=protein_to_node_dict[key]
        for v in value:
            D.add_node(id, predicate='location', label='location: ' + v, value=v,name=v,id=id)
            D.add_edge(id,neigh)
            D.add_edge(neigh,id)
            id=id+1

    for key, value in protein_class.iteritems():
        neigh=protein_to_node_dict[key]
        for v in value:
            D.add_node(id, predicate='protein_class', label='protein_class: ' + v, value=v,name=v,id=id)
            D.add_edge(id,neigh)
            D.add_edge(neigh,id)
            id=id+1

    for key, value in phenotype_dict.iteritems():
        neigh=protein_to_node_dict[key]
        for v in value:
            D.add_node(id, predicate='phenotype', label='phenotype: ' + v, value=v,name=v,id=id)
            D.add_edge(id,neigh)
            D.add_edge(neigh,id)
            id=id+1

    for key, value in interaction_dict.iteritems():
        neigh1=protein_to_node_dict[key]
        for ne in value:
            neigh2 = protein_to_node_dict[ne]
            D.add_node(id, predicate='interaction', label='interaction: ',name='interaction',id=id,value=True)
            D.add_edge(id,neigh1)
            D.add_edge(id,neigh2)
            id=id+1
    return D

if __name__ == '__main__':
    file_name_train = 'DATA/yeast/Folds/fold1/train.db'
    file_name_test = 'DATA/yeast/Folds/fold1/test.db'
    output_file_train = '/DATA/yeast/Folds/fold1/train.gpickle'
    output_file_test = '/DATA/yeast/Folds/fold1/test.gpickle'
    TrainGraph=parse_db_yeast(file_name_train)
    TestGraph = parse_db_yeast(file_name_train)
    nx.write_gpickle(TrainGraph,output_file_train)
    nx.write_gpickle(TestGraph,output_file_test)