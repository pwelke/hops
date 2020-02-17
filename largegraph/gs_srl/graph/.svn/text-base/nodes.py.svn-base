'''
Created on Mar 4, 2015

@author: irma
'''

"""
main class node
"""
import uuid
import time
import networkx as nx

class Node(object):
    #a label of a graph is predicate_name=unique identifier. more specific
    label=''
    #predicate is just a predicate name - more general
    predicate=''
    #target denotes if a node is one of the target nodes
    target=0
    #unique identifier of the node (different from the label name)
    id=0
    unique_value={}
    def __repr__(self):
        return str(self.label)
    
    def is_already_connected_to_unique_value(self,graph,node):
        return False
       
    def is_allowed_to_connect(self,node_id,node,graph):
        return None  

    def setId(self):
        self.id=uuid.uuid1().int>>64
        
    def get_predicates_connected_to_this_node(self,node_id,graph):
        predicates=[]
        for nb in nx.neighbors(graph,node_id):
            predicates.append(graph.node[nb]['predicate'])
        return predicates
    
    def setTarget(self):
        self.target=1
                
 
"""
Class representing a randvar-value test"""
class Randvar_value_test(Node): 
    value=''
    value_in_pattern=1
    object_predicate=[]
    
    def __init__(self,graph_node_representation=None,value=None,object_predicate=None):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        self.id=uuid.uuid1().int>>64
        self.value=value
        self.object_predicate=[object_predicate]
    
    def __repr__(self):
        return "randvar_value_test"
        #return "label: "+str(str(self.label)+" predicate: "+self.predicate+" value: "+str(self.value)+" value_in_pattern: "+str(self.value_in_pattern))
    
    def is_allowed_to_connect(self,node_id,node,graph):
        #print "NODE PREDICATE: ",node.predicate
        #print self.object_predicate
        #print "This node: ",self.predicate
        #print self,self.value
        #print "I am here: ",self.__class__
        #print node.predicate in self.object_predicate
        #print "Checking connection randvar value tests: "
        #if self.predicate in node.unique_value.keys():
        #    if self.predicate in node.get_predicates_connected_to_this_node(node_id,graph):
        #        return False  
        if(node.__class__==Randvar_value_test):
            return False
        #if(node.__class__==Object_class):
        #    return False
        #if(node.__class__==Relation):
        #    return False
        #print "pred: ",self.predicate," new node: ",node.predicate 
        #if (self.predicate==node.predicate):
        #    return False
        #if(not(isinstance(node,Object) or isinstance(node,Object_class))):
        #    return False
        #print "this node: ",self,self.predicate,"conn node: ",node,"have same predicates? ",node.predicate==self.object_predicate
        #if(self.object_predicate==None and node.object_predicate!=None):
        #    if(node.object_predicate==self.predicate):
        #        return True
        
        if(node.predicate in self.object_predicate):
            return True
        
        #if(node.is_allowed_to_connect(self.id,self,graph)):
        #    return True
        #if(node.object_predicate==self.predicate):
        #   return True
        else:
           return False
    
    def is_already_connected_to_unique_value(self,graph,node):
        return False
    
    def can_be_target_to(self,node):
        return False 
    
    def can_be_head(self):
        return False 
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return False 
    
    def to_string_representation(self):
      return "label: "+str(str(self.label)+" predicate: "+self.predicate+" value: "+str(self.value)+" value_in_pattern: "+str(self.value_in_pattern))
    
"""
Class representing a class of objects, e.g., proteins
"""
class Object_class(Node): 
    value_in_pattern=0
    def __init__(self,graph_node_representation=None):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        self.id=uuid.uuid1().int>>64
    
    def __repr__(self):
        return "object_class"
        #return "label: "+str(str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
    
    
    def is_already_connected_to_unique_value(self,graph,node):
        neighbours_of_node=nx.neighbors(graph,node)
        for neighb in neighbours_of_node:
            if graph.node[neighb]['predicate']==self.predicate and graph.node[neighb]['predicate'] in self.unique_value:
                return True
        return False
        
    def is_allowed_to_connect(self,node_id,node,graph):
        if isinstance(node, Randvar_value_test):
            if(node.object_predicate==self.predicate):
                return True
        if isinstance(node, Attribute):
            print "ATTRIBUTE!!!!",node.object_predicate,self.predicate
            if(node.object_predicate==self.predicate or self.predicate in node.object_predicate):
                return True
        if isinstance(node, Object):
            if(node.object_class_predicate==self.predicate):
                return True
        if isinstance(node, Relation):
            if(node.is_allowed_to_connect(node_id,self,graph)):
                return True  
        else:
            return False
    """
    For now??? object class nodes cannot be probabilistic predicate. They are just Logvars 
    """
    def can_be_target_to(self,node):
        return False
    
    def can_be_head(self):
        return False 
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return False
    
    def to_string_representation(self):
        return "label: "+str(str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
        
"""
Class representing a specific object, e.g., protein
"""
class Object(Node): 
    object_class_predicate=None
    value_in_pattern=0
    
    def __init__(self,graph_node_representation=None,object_class_predicate=None):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        #self.id=graph_node_representation['id']
        self.id=uuid.uuid1().int>>64
        self.object_class_predicate=object_class_predicate
    
    def __repr__(self):
       return "object"
       #return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
    
    def is_allowed_to_connect(self,node_id,node,graph):
        '''
        :param node: the node we are trying to connect to
        '''
        #print "object allowed to connect?",self.predicate," to? ",node, "should connect to: ",self.object_class_predicate,node.predicate==self.object_class_predicate['predicate']
        if(not(isinstance(node,Object_class) or isinstance(node,Object))):
            return False
        
        if(node.is_allowed_to_connect(self,self.id,graph)):
            return True
        #if (node.predicate==self.object_class_predicate):
        #        return True
        else:
            return False  
    
    """
    For now??? object value nodes cannot be probabilistic predicate. They are just Logvars 
    """
    def can_be_target_to(self,node):
        return False
    
    def can_be_head(self):
        return False  
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return True    
    
    def to_string_representation(self):
          return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
         
         
"""
Class representing a specific object, e.g., protein
"""
class Special_Object(Node): 
    object_class_predicate=None
    value_in_pattern=0
    
    def __init__(self,graph_node_representation=None,object_class_predicate=None):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        self.id=uuid.uuid1().int>>64
        self.object_class_predicate=object_class_predicate
    
    def __repr__(self):
       return "object"
       #return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
    
    def is_allowed_to_connect(self,node_id,node,graph):
        '''
        :param node: the node we are trying to connect to
        '''
        
        return True 
    
    """
    For now??? object value nodes cannot be probabilistic predicate. They are just Logvars 
    """
    def can_be_target_to(self,node):
        return False
    
    def can_be_head(self):
        return False  
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return True    
    
    def to_string_representation(self):
          return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))

"""
Class representing a specific object, e.g., protein
"""
class no_self_loop_object(Node): 
    object_class_predicate=None
    value_in_pattern=0
    
    def __init__(self,graph_node_representation=None,object_class_predicate=None):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        self.id=uuid.uuid1().int>>64
        self.object_class_predicate=object_class_predicate
    
    def __repr__(self):
       return "object"
       #return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
    
    def is_allowed_to_connect(self,node_id,node,graph):
        '''
        :param node: the node we are trying to connect to
        '''
        print node,node.predicate
        print self.id
        if node.predicate==self.predicate:
            print "return false"
            return False
        elif(node.__class__==self.__class__):
            return True
        elif(node.is_allowed_to_connect(self.id,self,graph)):
            return True
        #if (node.predicate==self.object_class_predicate):
        #        return True
        else:
            return False  
    
    
    """
    For now??? object value nodes cannot be probabilistic predicate. They are just Logvars 
    """
    def can_be_target_to(self,node):
        return False
    
    def can_be_head(self):
        return False  
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return True    
    
    def to_string_representation(self):
          return str("label: "+str(self.label)+" predicate: "+self.predicate+" target: "+str(self.target))
                  
         
         
"""
Class representing an attribute of a specific object, e.g., function of a protein
"""   
class Attribute(Node):
    value_in_pattern=0
    object_predicate=[] #Domain_object predicate name
    special=False #this denotes whn a relation node doesn't only connect to objects, but to other relation nodes
    #When specifying an attribute object, we should als know what its type object is.
    #E.g., attribute Intelligence of a Person
    unique=False
    
    def __init__(self,graph_node_representation,attribute_object_predicate):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        #self.id=graph_node_representation['id']
        self.id=uuid.uuid1().int>>64
        self.object_predicate=attribute_object_predicate
    
        
    def is_allowed_to_connect(self,node_id,node_type,graph):
        #print "attribute comparison, adding",node.predicate," attribute related to ",self.predicate
        #print "is this attribute unique to the node it is connecting to?",self.predicate in node.unique_value.keys()
        #if this attribute is unique to the node, and the node already has thi attribute connected to it, then don't allow connection
        #if self.predicate in node_type.unique_value.keys():
        #    if self.predicate in node_type.get_predicates_connected_to_this_node(node_id,graph):
        #        return False
            
        #if not self.special:
        #    if(not(isinstance(node_type,Object_class))): #PROBLEM HERE: in martin's examples "references" is not a relation. It can connect to dir. But also can connect to paper. CHECK THIS LATER
        #        return False
        #if self.unique==True and node.predicate==self.object_predicate and node.is_already_connected_to_unique_value(graph,self):
        #    return False
        if(node_type.predicate in self.object_predicate):
           return True
        else:
           return False
       
    def is_already_connected_to_unique_value(self,graph,node):
        return False

    def can_be_target_to(self,node):
        return True   
    
    def can_be_head(self):
        return True  
    
    def can_be_target(self):
        return True
    
    def __repr__(self):
        return "attribute"
    
    def canBeRoot(self):
        return True
    
    def to_string_representation(self):
        return "label: "+str(str(self.label)+" predicate: "+self.predicate+" object predicate: "+str(self.object_predicate)+" target: "+str(self.target))
    
"""
Relation node between two objects
"""      
class Relation(Node):
    value_in_pattern=0
    first_object_predicate=None #predicate of the first object in a relationship
    second_object_predicate=None #predicate of the second object in the relationship
    special=False #this denotes whn a relation node doesn't only connect to objects, but to other relation nodes
    argument_grounding=None
    #arg1=None
    #arg2=None
    

    def __init__(self,graph_node_representation,object1_predicate,object2_predicate):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        #self.id=graph_node_representation['id']
        self.id=uuid.uuid1().int>>64
        self.first_object_predicate=object1_predicate
        self.second_object_predicate=object2_predicate
    
    def __repr__(self):
        return "relation"    
    
    def are_allowed_to_connect_undirected(self,node1,node2):
        print "CHECK: ",node1,node2
        print "First objects: ",self.first_object_predicate,self.second_object_predicate
        if (node1==self.first_object_predicate and node2==self.second_object_predicate) or (node1==self.second_object_predicate and node2==self.first_object_predicate):
            return True
        else:
            return False
    
    def is_already_connected_to_unique_value(self,graph,node):
        return False
    
    def is_allowed_to_connect(self,node_id,node,graph):
        if(isinstance(node,Randvar_value_test)):
            return False
        
        try:
           neighbours=graph.neighbors(node_id)
        except:                 
           neighbours=[]
#         print "NODE:",node
#         print "nr neighbors: ",len(neighbours)
#         print "self id :",self.id
#         print "graph: "
        for n in graph.nodes():
            print graph.node[n]
            print n
        #print "Trying to connect: ",node.predicate,"to ",self.predicate
        arg1=None
        arg2=None
        if len(neighbours)==2:
            arg1=graph.node[neighbours[0]]['predicate']
            arg2=graph.node[neighbours[1]]['predicate']
        if len(neighbours)==1:
            arg1=graph.node[neighbours[0]]['predicate']            
        
        #if(not(isinstance(node,Object_class))):
        #    return False
#         if (self.first_object_predicate!=self.second_object_predicate):
#             #print "nodes in graph:"
#             #for node in graph.nodes():
#             #  print node,graph.node[node]  
#             #print "this node id: ",self.id,self
#             try:
#                 neighbours=graph.neighbors(self.id)
#             except: 
#                 neighbours=[]
#             for n in neighbours:
#                 if graph.node[n]['predicate']==node.predicate:
#                     return False
#                 else:
#                     return True
        
        #print "fir sobj: ",self.first_object_predicate
        #print "sec onj ",self.second_object_predicate
        #print "Args: "
        #print arg1
        #print arg2
        if((node.predicate==self.first_object_predicate) | (node.predicate==self.second_object_predicate)):
            if(self.first_object_predicate==self.second_object_predicate):
                return True 
            if(self.first_object_predicate!=self.second_object_predicate):
                    #print "trying to connecT: ",node.predicate
                    #print self.arg1
                    #print self.arg2
                    #print "**********************************************"
                    if node.predicate==arg1 or node.predicate==arg2:
                        return False
                    else:
                        #self.argument_grounding=node.predicate
                        return True
        return False
        
    #apparently relations cannot be targets, had problems with interaction    
    def can_be_target_to(self,node):
        return False 
    
    def can_be_head(self):
        return False 
    
    def can_be_target(self):
        return False
    
    def canBeRoot(self):
        return True
    
    def to_string_representation(self):
        return str("label: "+self.label+" predicate: "+self.predicate+" "+"rel:"+str(self.first_object_predicate)+"-"+str(self.label)+"-"+str(self.second_object_predicate))   
    
#if __name__ == '__main__':
#     protein=Domain_object('protein','protein',0)
#     function=Attribute('function','function',0,protein)
#     location=Attribute('location','location',0,protein)
#     interaction=Relation('interaction','interaction',0,protein,protein)
#     
#     print protein.is_allowed_to_connect(function)
#     print protein.is_allowed_to_connect(protein)
#     print interaction.is_allowed_to_connect(protein)
#     print interaction.is_allowed_to_connect(function)