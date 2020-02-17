import networkx as nx


def parse_line(line):
   out=line.split('(')
   predicate_name=out[0].lstrip().rstrip()
   arguments=out[1].split(',')
   arg1=arguments[0].replace(".","").rstrip().lstrip()
   arg2=arguments[1].replace(".","").replace(")","").lstrip().rstrip()
   return predicate_name,arg1,arg2

def parse_db_imdb(file_name):
    movies = {}
    actors = {}
    directors = {}
    worked_under = {}
    genre = {}
    associated_person = {}
    gender = {}
    id = 0
    same_gender = {}
    D = nx.Graph()

    with open(file_name, 'r') as f:
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
                if gender_1 in same_gender:
                    same_gender[gender_1].append(id)
                else:
                    same_gender[gender_1] = []
                    same_gender[gender_1].append(id)
            if "genre" in line:
                obj1 = line[line.find("(") + 1:line.find(",")]  # person
                genre_1 = line[line.find(",") + 1:line.find(")")].rstrip().lstrip()
                genre[obj1] = genre_1
            id += 1
    id=0
    actor_to_node={}
    movie_to_node = {}
    director_to_node = {}
    for p in actors:
        D.add_node(id,predicate='actor',label='actor: '+p,value=p,name=p,id=id)
        actor_to_node[p]=id
        id=id+1

    for p in movies:
        D.add_node(id,predicate='movie',label='movie: '+p,value=p,name=p,id=id)
        movie_to_node[p]=id
        id=id+1

    for p in directors:
        D.add_node(id,predicate='director',label='director: '+p,value=p,name=p,id=id)
        director_to_node[p]=id
        id=id+1

    for a in actors:
        actor_node=actor_to_node[a]
        p=gender[a]
        D.add_node(id, predicate='gender', label='gender: ' + p, value=p, name=p, id=id)
        D.add_edge(actor_node, id)
        id = id + 1

    for d in directors:
        director_node=director_to_node[d]
        if d in genre:
            p=genre[d]
            D.add_node(id, predicate='genre', label='genre: ' + p, value=p, name=p, id=id)
            D.add_edge(director_node, id)
            id = id + 1

    for a in worked_under:
        for d in worked_under[a]:
            D.add_node(id, predicate='workedUnder', label='workedUnder: ' + p, value=True, name=True, id=id)
            D.add_edge(actor_to_node[a], id)
            D.add_edge(id, director_to_node[d])
            id = id + 1

    for m in associated_person:
        for a in associated_person[m]:
            D.add_node(id, predicate='actsIn', label='actsIn: ' + p, value=True, name=True, id=id)
            if a in actor_to_node:
               D.add_edge(actor_to_node[a], id)
            elif d in director_to_node:
               D.add_edge(director_to_node[d], id)
            D.add_edge(id, movie_to_node[m])
            id = id + 1


    return D

if __name__ == '__main__':
    file_name_train = '/DATA/IMDB/folds/fold1/train.db'
    file_name_test = '/DATA/IMDB/folds/fold1/test.db'
    output_file_train = '/DATA/IMDB/folds/fold1/train.gpickle'
    output_file_test = '/DATA/IMDB/folds/fold1/test.gpickle'
    TrainGraph=parse_db_imdb(file_name_train)
    TestGraph = parse_db_imdb(file_name_test)
    nx.write_gpickle(TrainGraph,output_file_train)
    nx.write_gpickle(TestGraph,output_file_test)