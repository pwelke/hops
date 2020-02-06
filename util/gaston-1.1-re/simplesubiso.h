// misc.h
// Siegfried Nijssen, snijssen@liacs.nl, jul 2004.
#ifndef SIMPLESUBISO_H
#define SIMPLESUBISO_H
#include "subgraphiso.h"

class SimpleSubIso:public SubGraphIso {
  private:
    int *temp;
    int g1size, g2size;
    
    int g1actionssize;
    bool found;
    PATMASKTYPE usedmark, usemark;
    NodeId lastnode;
    int btdepth;
    vector<NodeId> bttomark;
    int startnodes[MAXPATSIZE];

    bool isEdge ( NodeId node1, NodeId node2, EdgeLabel label );
    void recurse ( int acti, int tonode, int d );
  public:
    struct Action { 
      bool close;
      NodeId connectfrom, connectto;
      EdgeLabel edgelabel;
    };
    Action *g1actions;
    
    SimpleSubIso ();
    ~SimpleSubIso ();
    void init ( int maxnredges, int maxnrnodes );
    void prepare ();
    bool run ( DatabaseTree *databasetree );
};

extern SimpleSubIso *simplesubiso;

#endif
