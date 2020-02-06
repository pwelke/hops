GCC=g++ -O3
ALLFILES=legmanager.cpp tidlist.cpp main.cpp database.cpp database.h misc.h patterntree.cpp patterntree.h patterngraph.cpp patterngraph.h graphstate.cpp graphstate.h subgraphiso.cpp simplesubiso.cpp
OBJS=subgraphiso.o simplesubiso.o main.o legmanager.o tidlist.o database.o path.o patterntree.o patterngraph.o graphstate.o 
gaston: $(OBJS)
	$(GCC) -o gaston $(OBJS)
clean:
	rm $(OBJS); rm gaston
database.o: database.cpp database.h
	$(GCC) -c database.cpp
database.h: legoccurrence.h misc.h
patterntree.o: patterntree.cpp patterntree.h patterngraph.h graphstate.h
	$(GCC) -c patterntree.cpp
patterntree.h: misc.h database.h legoccurrence.h path.h 
patterngraph.o: patterngraph.cpp patterngraph.h graphstate.h
	$(GCC) -c patterngraph.cpp
main.o: misc.h database.h main.cpp path.h graphstate.h
	$(GCC) -c main.cpp
path.o: path.cpp path.h patterntree.h patterngraph.h graphstate.h
	$(GCC) -c path.cpp
path.h: misc.h database.h legoccurrence.h
graphstate.o: graphstate.cpp graphstate.h database.h misc.h
	$(GCC) -c graphstate.cpp 
graphstate.h: misc.h 
legmanager.o: legmanager.cpp legmanager.h
	$(GCC) -c legmanager.cpp
tidlist.o: tidlist.cpp tidlist.h
	$(GCC) -c tidlist.cpp
subgraphiso.o: subgraphiso.cpp subgraphiso.h
	$(GCC) -c subgraphiso.cpp
simplesubiso.o: simplesubiso.cpp simplesubiso.h subgraphiso.h
	$(GCC) -c simplesubiso.cpp
