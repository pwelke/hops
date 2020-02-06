// subgraphiso.h
// Siegfried Nijssen, snijssen@liacs.nl, jul 2004.
#ifndef SUBGRAPHISO_H
#define SUBGRAPHISO_H
#include "database.h"

/**
@author Siegfried Nijssen
This class is only virtual. Other classes must implement it.
*/
class SubGraphIso{
public:
    SubGraphIso();

    virtual ~SubGraphIso();
    vector<NodeId> changednodes;  
      // If an occurrence is found, this set contains the indexes of the
      // nodes in the pattern graph for which the mapping has changed since
      // the previous mapping, and furthermore are still interesting 
      // according to the legmanager.
    int *used;
      // for each node in the current database graph,
      // used[i] == 0 means that the node in the database graph is not mapped
      //              to in the current mapping
      // otherwise: used[i]-1 is the index of the node in the current pattern
      //            graph that is currently mapped to this node
    int *map;
      // for each node in the current pattern graph, the node in the database
      // graph to which it is mapped.
    DatabaseTree *databasetree;
      // the tree to which the algorithm is currently applied
    
    virtual void init ( int maxnredges, int maxnrnodes ) = 0;
      // subgraphiso objects should be created once, and initialized
      // after the largest possible graph is known. Use this function
      // to initialize
    
    virtual void prepare () = 0;
      // the algorithm may first determine a strategy for the current
      // graph in the graphstate, before going through graphs in the database
    
      // run the subgraph isomorphism algorithm on the algorithm in the current
      // graphstate
      // This function calls the leg manager update functions as required.
      // The leg manager expects the changed nodes and used fields to be
      // filled in correctly
    virtual bool run ( DatabaseTree *databasetree ) = 0;
};

#endif
