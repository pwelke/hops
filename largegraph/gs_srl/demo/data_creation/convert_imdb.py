'''
Created on Sep 26, 2016

@author: irma
'''
'''
Created on Sep 6, 2016

@author: irma
'''
import networkx as nx



FILE_NAME = "/home/irma/work/DATA/DATA/IMDB/imdb_folds/fold1/train.gpickle"
imdb_input = '/home/irma/work/DATA/DATA/IMDB/imdb_folds/fold1/train.db'

movies = {}
actors = {}
directors = {}
worked_under = {}
genre = {}
associated_person = {}
gender = {}
id = 0
same_gender = {}

with open(imdb_input, 'r') as f:
    for line in f.readlines():
        if "actor" in line:
            actors[line[line.find("(") + 1:line.find(")")].rstrip().lstrip()] = id
        if "movie" in line:
            movie = line[line.find("(") + 1:line.find(",")].rstrip().lstrip()
            movies[movie] = id
            if movie in associated_person:
                associated_person[movie].append(line[line.find(",") + 1:line.find(")")].rstrip().lstrip())
            else:
                associated_person[movie] = [line[line.find(",") + 1:line.find(")")].rstrip().lstrip()]
        if "director" in line:
            directors[line[line.find("(") + 1:line.find(")")].rstrip().lstrip()] = id
        if "workedUnder" in line:
            obj1 = line[line.find("(") + 1:line.find(",")].rstrip().lstrip()
            obj2 = line[line.find(",") + 1:line.find(")")].rstrip().lstrip()
            if obj1 in worked_under:
                worked_under[obj1].append(obj2)
            else:
                worked_under[obj1] = [obj2]
        if "gender" in line:
            obj1 = line[line.find("(") + 1:line.find(",")].rstrip().lstrip()
            gender_1 = line[line.find(",") + 1:line.find(")")].rstrip().lstrip()
            gender[obj1] = gender_1
        if "genre" in line:
            obj1 = line[line.find("(") + 1:line.find(",")]  # person
            genre_1 = line[line.find(",") + 1:line.find(")")].rstrip().lstrip()
            # print obj1,genre
            if obj1 in genre:
                genre[obj1].append(genre_1)
            else:
                genre[obj1] = [genre_1]
        id += 1

D=nx.Graph()
id=0
actor_to_node={}
movie_to_node={}
director_to_node={}

for a in actors:
    D.add_node(id, predicate='actor', label='actor: ' + a, value=a, name=a, id=id)
    actor_to_node[a] = id
    id = id + 1

for m in movies:
    D.add_node(id, predicate='movie', label='movie: ' + m, value=m, name=m, id=id)
    movie_to_node[m] = id
    id = id + 1

for d in directors:
    D.add_node(id, predicate='director', label='director: ' + d, value=d, name=d, id=id)
    director_to_node[d] = id
    id = id + 1


for key, value in gender.iteritems():
        node=None
        if key in actors:
          node=actor_to_node[key]
        if key in directors:
          node=director_to_node[key]
        for v in value:
            D.add_node(id, predicate='gender', label='gender: ' + v, value=v,name=v,id=id)
            D.add_edge(id,node)
            D.add_edge(node,id)
            id=id+1


for key, value in gender.iteritems():
        node=None
        if key in actors:
          node=actor_to_node[key]
        if key in directors:
          node=director_to_node[key]
        for v in value:
            D.add_node(id, predicate='gender', label='gender: ' + v, value=v,name=v,id=id)
            D.add_edge(id,node)
            D.add_edge(node,id)
            id=id+1

for key, value in genre.iteritems():
        node=None
        if key in movies:
          node=movie_to_node[key]
        if key in directors:
          node=director_to_node[key]
        for v in value:
            D.add_node(id, predicate='genre', label='genre: ' + v, value=v,name=v,id=id)
            D.add_edge(id,node)
            D.add_edge(node,id)
            id=id+1

for key, value in associated_person.iteritems():
        movie=movie_to_node[key]
        for ne in value:
            if ne in actors:
                person=actor_to_node[ne]
                pred="actsIn"
            if ne in directors:
                neigh2=director_to_node[ne]
                pred="directed"
            D.add_node(id, predicate=pred, label=pred,name=pred,id=id,value=True)
            D.add_edge(id,movie)
            D.add_edge(person,id)
            id=id+1

for key, value in worked_under.iteritems():
        actor=actor_to_node[key]
        for ne in value:
            dir=director_to_node[ne]
            D.add_node(id, predicate='workedUnder', label='workedUnder: ',name="workedUnder",id=id,value=True)
            D.add_edge(id,actor)
            D.add_edge(actor, id)
            id=id+1

nx.write_gpickle(D,FILE_NAME)


