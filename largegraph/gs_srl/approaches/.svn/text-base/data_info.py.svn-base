'''
Created on Oct 4, 2016

@author: irma
'''
import networkx as nx
import graph_manipulator.graph_analyzer as an

# data=nx.read_gpickle('/home/irma/workspace/Martin_experiments/DBLP/dblp.gpickle')
# print "Nr nodes DBLP: ",len(data.nodes())
# print "Nr edges DBPL: ",len(data.edges())
# print "Max degree: ",an.get_maximum_node_degree(data)
# print "Density: ",nx.density(data)
# print "INFO:",nx.info(data)
# 
# 
# #WEBKB
# print "-------------------------------------------"
# data=nx.read_gml('/home/irma/workspace/some_scripts_martin_sampling/DATA/webkb/webkb.gml')
# print "Nr nodes WEBKB: ",len(data.nodes())
# print "Nr edges WEBKB: ",len(data.edges())
# print "Max degree WEBKB: ",an.get_maximum_node_degree(data)
# print "Density WEBKB: ",nx.density(data)
# print "INFO WEBKB:",nx.info(data)
# 
# #IMDB
# print "-------------------------------------------"
# data=nx.read_gml('/home/irma/workspace/some_scripts_martin_sampling/DATA/imdb/imdb.gml')
# print "Nr nodes IMDB: ",len(data.nodes())
# print "Nr edges IMDB: ",len(data.edges())
# print "Max degree IMDB: ",an.get_maximum_node_degree(data)
# print "Density IMDB: ",nx.density(data)
# print "INFO IMDB:",nx.info(data)
# 
# print "-------------------------------------------"
# 
# #YEAST
# data=nx.read_gpickle('/home/irma/workspace/some_scripts_martin_sampling/DATA/yeast/yeast.gpickle')
# print "Nr nodes YEAST: ",len(data.nodes())
# print "Nr edges YEAST: ",len(data.edges())
# print "Max degree YEAST: ",an.get_maximum_node_degree(data)
# print "Density YEAST: ",nx.density(data)
# print "INFO YEAST:",nx.info(data)

#Facebook
# data=nx.read_gpickle('/data/leuven/311/vsc31168/MARTIN_EXPERIMENTS/DATA/AMAZON/amazon.gpickle')
# print "Nr nodes Facebook: ",len(data.nodes())
# print "Nr edges Facebook: ",len(data.edges())
# print "Max degree Facebook: ",an.get_maximum_node_degree(data)
# print "Density Facebook: ",nx.density(data)
# print "INFO Facebook:",nx.info(data)

#given two files containing paths, detect the paths that are the difference of the two files
def detect_missing_paths(doc1,doc2,remove1,remove2):
    set_paths1=[]
    set_paths2=[]
    with open(doc1,'r') as f:
        for line in f.readlines():
            set_paths1.append(line.replace(remove1,""))
    with open(doc2,'r') as f:
        for line in f.readlines():
            set_paths2.append(line.replace(remove2,""))
    print "The difference:"
    print len(set_paths1)
    print len(set_paths2)
    for e in list(set(set_paths2) - set(set_paths1)):
        print e

if __name__=="__main__":
    detect_missing_paths("/home/irma/doc1.txt","/home/irma/doc2.txt","results_false_furer_order_random","results_false_furer")
    