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

    def is_allowed_to_connect(self,node_id,node,graph):
        if(node.__class__==Randvar_value_test):
            return False
        if(node.predicate in self.object_predicate):
            return True

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
        if node.predicate==self.predicate:
            return False
        elif(node.__class__==self.__class__):
            return True
        elif(node.is_allowed_to_connect(self.id,self,graph)):
            return True
        #if (node.predicate==self.object_class_predicate):
        #        return True
        else:
            return False  

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
            self.id=uuid.uuid1().int>>64
        self.object_predicate=attribute_object_predicate
    
        
    def is_allowed_to_connect(self,node_id,node_type,graph):
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

    def __init__(self,graph_node_representation,object1_predicate,object2_predicate):
        self.label=graph_node_representation['label']
        self.predicate=graph_node_representation['predicate']
        if(not('target' in graph_node_representation)):
            self.target=0
        else:
            self.target=graph_node_representation['target']
        self.id=uuid.uuid1().int>>64
        self.first_object_predicate=object1_predicate
        self.second_object_predicate=object2_predicate
    
    def __repr__(self):
        return "relation"    
    
    def are_allowed_to_connect_undirected(self,node1,node2):
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
        arg1=None
        arg2=None
        if len(neighbours)==2:
            arg1=graph.node[neighbours[0]]['predicate']
            arg2=graph.node[neighbours[1]]['predicate']
        if len(neighbours)==1:
            arg1=graph.node[neighbours[0]]['predicate']            

        if((node.predicate==self.first_object_predicate) | (node.predicate==self.second_object_predicate)):
            if(self.first_object_predicate==self.second_object_predicate):
                return True 
            if(self.first_object_predicate!=self.second_object_predicate):
                    if node.predicate==arg1 or node.predicate==arg2:
                        return False
                    else:
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
    
