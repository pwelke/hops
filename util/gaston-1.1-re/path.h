// path.h
// Siegfried Nijssen, snijssen@liacs.nl, jan 2004.
#ifndef PATH_H
#define PATH_H
#include <iostream>
#include <vector>
#include "misc.h"
#include "database.h"
#include "legmanager.h"
//#include "patterntree.h"

using namespace std;

class Path {
  public:
    Path ( DatabaseEdgeLabel &databaseedgelabel );
    ~Path ();
    void expand ();
  private:
    TidList *tidlist;
    bool isnormal ( EdgeLabel edgelabel ); // ADDED
    friend class PatternTree;
    void expand2 ();
    Path ( Path &parentpath, unsigned int legindex );
    vector<Leg> legs; 
    vector<CloseLeg> closelegs;
    vector<NodeLabel> nodelabels;
    vector<EdgeLabel> edgelabels;
    int frontsymmetry; // which is lower, the front or front reverse?
    int backsymmetry; // which is lower, the back or back reverse?
    int totalsymmetry; // which is lower, from left to right, or the reverse?

    friend ostream &operator<< ( ostream &stream, Path &path );
};

#endif
