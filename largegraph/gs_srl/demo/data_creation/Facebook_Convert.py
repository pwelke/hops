'''
Created on Oct 4, 2016

@author: irma
'''
import graph.visualization as vis
import networkx as nx

FILE_NAME = "/home/irma/workspace/DATA/Facebook/facebook.gml"
users_and_edges="/home/irma/workspace/DATA/Facebook/facebook_combined.txt"

users_list=[]
edges_map={}
nr_edges=0



with open(users_and_edges,'r') as f:
    for line in f.readlines():
        users=line.rstrip().lstrip().split(" ") 
        if not users[0] in users_list:
            users_list.append(users[0])
        if not users[1] in users_list:
            users_list.append(users[1])
        if users[0] in edges_map:
            edges_map[users[0]].append(users[1])
        else:
            edges_map[users[0]]=[users[1]]
        
        nr_edges+=1

links=0

for user in edges_map.keys():
       for user2 in edges_map[user]:
          links+=1

ego_users=[0, 107,348,414,686,1684,1912,3437,3980]
birthday_indices={}
education_type_indices={}
education_degree_indices={}
gender_indices={}
hometown_indices={}
language_indices={}
features={}

bitrthday_ids={}
education_type_ids={}
education_degree_ids={}
gender_ids={}
hometown_ids={}
language_ids={}
features_ids={}

birthdays={}
education_types={}
education_degrees={}
gender={}
hometown={}
language={}


for e in ego_users:
    with open("/home/irma/workspace/DATA/Facebook/facebook/"+str(e)+".featnames",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            ft_name=fts[1]
            if "birthday" in ft_name:
                if str(e) in birthday_indices:
                    birthday_indices[str(e)].append(int(fts[0]))
                    bitrthday_ids[str(e)].append(int(fts[-1]))
                else:
                    birthday_indices[str(e)]=[int(fts[0])]
                    bitrthday_ids[str(e)]=[int(fts[-1])]
            
            if "education;type" in ft_name:
                if str(e) in education_type_indices:
                    education_type_indices[str(e)].append(int(fts[0]))
                    education_type_ids[str(e)].append(int(fts[-1]))
                else:
                    education_type_indices[str(e)]=[int(fts[0])]
                    education_type_ids[str(e)]=[int(fts[-1])]
                    
            if "gender" in ft_name:
                if str(e) in gender_indices:
                    gender_indices[str(e)].append(int(fts[0]))
                    gender_ids[str(e)].append(int(fts[-1]))
                else:
                    gender_indices[str(e)]=[int(fts[0])]
                    gender_ids[str(e)]=[int(fts[-1])]
                    
            if "education;degree" in ft_name:
                if str(e) in education_degree_indices:
                    education_degree_indices[str(e)].append(int(fts[0]))
                    education_degree_ids[str(e)].append(int(fts[-1]))
                else:
                    education_degree_indices[str(e)]=[int(fts[0])]  
                    education_degree_ids[str(e)]=[int(fts[-1])]  
            
            if "hometown" in ft_name:
                if str(e) in hometown_indices:
                    hometown_indices[str(e)].append(int(fts[0]))
                    hometown_ids[str(e)].append(int(fts[-1]))
                else:
                    hometown_indices[str(e)]=[int(fts[0])] 
                    hometown_ids[str(e)]=[int(fts[0])]    
                    
            if "language" in ft_name:
                if str(e) in language_indices:
                    language_indices[str(e)].append(int(fts[0]))
                    language_ids[str(e)].append(int(fts[-1]))
                else:
                    language_indices[str(e)]=[int(fts[0])]   
                    language_ids[str(e)]=[int(fts[-1])]    

alter_to_ego={}
edges={}

nr_links=0

for e in ego_users:
    with open("/home/irma/workspace/DATA/Facebook/facebook/"+str(e)+".feat",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            features[fts[0]]=fts[1:] 
            alter_to_ego[str(fts[0])]=str(e)
           
                
            
    with open("/home/irma/workspace/DATA/Facebook//facebook/"+str(e)+".egofeat",'r') as f:
        for line in f.readlines():
            fts=line.rstrip().split(" ")
            features[str(e)]=fts
            alter_to_ego[str(e)]=str(e)


user_birthday={}
user_hometown={}
user_education_type={}
user_education_degree={}
user_gender={}
user_language={}

gender_unknown=0
hometown_unknown=0
education_type_unknown=0
education_degree_unknown=0
birthday_unknown=0
language_unknown=0


for user in features.keys():
    ego_index=alter_to_ego[user]
    user_feature=features[user]
    try:
      birthday_index = [user_feature[i] for i in birthday_indices[ego_index]].index('1')
      birthday_count = [user_feature[i] for i in birthday_indices[ego_index]].count('1')
      user_birthday[user]=bitrthday_ids[ego_index][birthday_index]
      if birthday_count>1:
         print("WARNING BIRTHDAY!!!")
    except:
        birthday_index=-1
        birthday_unknown+=1
        user_birthday[user]="unknown"
    try:
      gender_index = [user_feature[i] for i in gender_indices[ego_index]].index('1')
      gender_count = [user_feature[i] for i in gender_indices[ego_index]].count('1')
      user_gender[user]=gender_ids[ego_index][gender_index]
      if(gender_count>1):
          print("WARNING GENDER!")
    except:
      gender_index=-1
      gender_unknown+=1
      user_gender[user]="unknown"
    #print ego_index,user,hometown_indices[ego_index],[user_feature[i] for i in hometown_indices[ego_index]]
    try:
      hometown_index = [user_feature[i] for i in hometown_indices[ego_index]].index('1')
      hometown_count = [user_feature[i] for i in hometown_indices[ego_index]].count('1')
      user_hometown[user]=hometown_ids[ego_index][hometown_index]
      if hometown_count>1:
          print("WARNING HOMETOWN")
    except:
      hometown_index=-1
      hometown_unknown+=1
      user_hometown[user]="unknown"
    try:
      education_type_index = [user_feature[i] for i in education_type_indices[ego_index]].index('1')
      education_type_count = [user_feature[i] for i in education_type_indices[ego_index]].count('1')
      user_education_type[user]=education_type_ids[ego_index][education_type_index]
    except:
      education_type_index=-1
      education_type_unknown+=1
      user_education_type[user]="unknown"
    try:
       if ego_index!=686: #no education degree for this circle
          education_degree = [user_feature[i] for i in education_degree_indices[ego_index]].index('1')
          education_degree_count = [user_feature[i] for i in education_degree_indices[ego_index]].count('1')
          user_education_degree[user]=education_degree_ids[ego_index][education_degree]
    except:
          education_degree=-1
          education_degree_unknown+=1
          user_education_degree[user]="unknown"
    try: 
       language_index=[user_feature[i] for i in language_indices[ego_index]].index('1')
       language_count = [user_feature[i] for i in language_indices[ego_index]].count('1')
       user_language[user]=language_ids[ego_index][language_index]
    except:
        language_index=-1
        language_unknown+=1
        user_language[user]="unknown"

f = open(FILE_NAME, "w")

# #helpers
s = " "
ss = s+s
sss = s+s+s
ssss = s+s+s+s
nl = "\n"
  
#loop helpers
added = []
ind = 0

#Root node
f.write("graph"+nl)
f.write("["+nl)
  
#Write an edge

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out


def get_edge_string(source,target):
    result=""
    result+= ss + "edge" + nl
    result+= ss + "[" + nl
    result+= ssss + "source" + s + str(source) + nl
    result+= ssss + "target" + s + str(target) + nl
    result+= ss + "]"+ nl
    return result

def write_edge(source,target):
    f.write( ss + "edge" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "source" + s + str(source) + nl)
    f.write( ssss + "target" + s + str(target) + nl)
    f.write( ss + "]"+ nl)
  
#Write a node
def write_node(predicate,label,id):
    f.write( ss + "node" + nl)
    f.write( ss + "[" + nl)
    f.write( ssss + "id" + s + str(id)  + nl)
    f.write( ssss + "value" + s + '"' + label + '"' + nl)
    f.write( ssss + "predicate" + s + '"' + predicate + '"' + nl)
    f.write( ssss + "label" + s + '"' + label + '"' + nl)
    f.write( ss + "]"+ nl)
    
nr_users=0
user_ids={}
id=0    
for user in users_list:
    nr_users+=1
    write_node("user","user",str(user))
    user_ids[user]=id
    id+=1



birthdays=0
hometowns=0
education_types=0
education_degrees=0
genders=0
languages=0

feature_edges=""

birthday_values=[]
hometown_values=[]
education_type_values=[]
education_degree_values=[]
language_values=[]
gender_values=[]

#write birthdays
#split birthdays into three categories
for user in user_birthday.keys():
    if not str(user_birthday[user]) in birthday_values:
        birthday_values.append(str(user_birthday[user]))        
birthday_categories=chunkIt(birthday_values, 3)

for user in user_birthday.keys():
    if str(user_birthday[user]) in birthday_categories[0]:
        write_node("birthday","value_1",str(id))
    
    if str(user_birthday[user]) in birthday_categories[1]:
        write_node("birthday","value_2"+str(user_birthday[user]),str(id))
        
    if str(user_birthday[user]) in birthday_categories[2]:
        write_node("birthday","value_3",str(id))
        
    feature_edges+=get_edge_string(user_ids[user],str(id))
    birthdays+=1
    id+=1
 
 
 #write hometowns
for user in user_hometown.keys():
    if not str(user_hometown[user]) in hometown_values:
        hometown_values.append(str(user_hometown[user]))        
hometown_categories=chunkIt(hometown_values, 3) 
 
for user in user_hometown.keys():
     if str(user_hometown[user]) in hometown_categories[0]:
        write_node("hometown","value_1",str(id))
     if str(user_hometown[user]) in hometown_categories[1]:
        write_node("hometown","value_2",str(id))
     if str(user_hometown[user]) in hometown_categories[2]:
        write_node("hometown","value_3",str(id))
     feature_edges+=get_edge_string(user_ids[user],str(id))
     hometowns+=1
     id+=1
 
#write education type
for user in user_education_type.keys():
    if not str(user_education_type[user]) in education_type_values:
        education_type_values.append(str(user_education_type[user]))        
education_type_categories=chunkIt(education_type_values, 3) 

for user in user_education_type.keys():
     if str(user_education_type[user]) in education_type_categories[0]:
        write_node("education_type","value_1",str(id))
     if str(user_education_type[user]) in education_type_categories[1]:
        write_node("education_type","value_2",str(id))
     if str(user_education_type[user]) in education_type_categories[2]:
        write_node("education_type","value_3",str(id))
     feature_edges+=get_edge_string(user_ids[user],str(id))
     education_types+=1
     id+=1
     
for user in user_education_degree.keys():
    if not str(user_education_degree[user]) in education_degree_values:
        education_degree_values.append(str(user_education_degree[user]))        
education_degree_categories=chunkIt(education_degree_values, 3)
 
 #write education degree
for user in user_education_degree.keys():
     if str(user_education_degree[user]) in education_degree_categories[0]:
         write_node("education_degree","value_1",str(id))
     if str(user_education_degree[user]) in education_degree_categories[1]:
         write_node("education_degree","value_2",str(id))
     if str(user_education_degree[user]) in education_degree_categories[2]:
         write_node("education_degree","value_3",str(id))
     feature_edges+=get_edge_string(user_ids[user],str(id))
     education_degrees+=1
     id+=1
     
 
 #write gender
for user in user_gender.keys():
     write_node("gender","value_"+str(user_gender[user]),str(id))
     if not "value_"+str(user_gender[user]) in gender_values:
         gender_values.append("value_"+str(user_gender[user]))
     feature_edges+=get_edge_string(user_ids[user],str(id))
     genders+=1
     id+=1
  
 #write language
for user in user_language.keys():
    if not str(user_language[user]) in language_values:
        language_values.append(str(user_language[user]))        
education_degree_categories=chunkIt(language_values, 3)


for user in user_language.keys():
     if str(user_language[user]) in language_values[0]:
         write_node("language","value_1",str(id))
     if str(user_language[user]) in language_values[1]:
         write_node("language","value_2",str(id))
     if str(user_language[user]) in language_values[2]:
         write_node("language","value_3",str(id))
     feature_edges+=get_edge_string(user_ids[user],str(id))
     languages+=1
     id+=1
     


 
links=0
for user in edges_map.keys():
        for user2 in edges_map[user]:
           write_edge(str(user),str(user2))
           links+=1

f.write(feature_edges)
 
f.write("]"+nl)
f.close()
 
graph=nx.read_gml(FILE_NAME)
vis.visualize_graph_standard(graph)
    
    
    
    

