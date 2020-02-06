// patterngraph.h
// Siegfried Nijssen, snijssen@liacs.nl, jan 2004.
#ifndef PATTERNGRAPH_H
#define PATTERNGRAPH_H
#include <vector>
#include "legmanager.h"
#include "tidlist.h"

using namespace std;

class PatternGraph {
  public:
    vector<CloseLeg> closelegs;
    vector<CloseLeg> closetuples;
    void init ( vector<CloseLeg> &closelegssource, int legindex, TidList *ptidlist );
    PatternGraph  ( vector<CloseLeg> &closelegssource, int legindex, TidList *tidlist ) {
      init ( closelegssource, legindex, tidlist );
    }
    PatternGraph  ( PatternGraph &parentpatterngraph, int legindex ):
      closetuples ( parentpatterngraph.closetuples ) {
      init ( parentpatterngraph.closelegs, legindex, parentpatterngraph.tidlist );
    }
    TidList *tidlist, *ptidlist;
    vector<CloseLeg> *closelegssource;
    int legindex;
    Frequency frequency; 
    ~PatternGraph ();
    void expand ();
};

#endif
