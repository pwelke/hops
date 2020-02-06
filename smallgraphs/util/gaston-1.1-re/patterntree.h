// patterntree.h
// Siegfried Nijssen, snijssen@liacs.nl, jan 2004.
#ifndef PATTERNTREE_H
#define PATTERNTREE_H
#include <iostream>
#include <vector>
#include "misc.h"
#include "database.h"
#include "path.h"
#include "tidlist.h"
#include "legmanager.h"

using namespace std;

class PatternTree {
  public:
    PatternTree ( Path &path, unsigned int legindex );
    ~PatternTree ();
    void expand ();
  private:
    void checkIfIndeedNormal ();
    /* inline */ void addExtensionLegs ( Leg &tuple );
    /* inline */ void addLeg ( const NodeId connectingnode, const int depth, const EdgeLabel edgelabel );
    /* inline */ void addLeftLegs ( Path &path, Leg &leg, int &i, Depth olddepth, EdgeLabel lowestlabel, int leftend, int edgesize2 );
    /* inline */ int addLeftLegs ( Path &path, Leg &leg, Leg &leg2, unsigned int legindex, int leftend, int edgesize2 );
    /* inline */ void addRightLegs ( Path &path, Leg &leg, int &i, Depth olddepth, EdgeLabel lowestlabel, int rightstart, int nodesize2 );
    /* inline */ int addRightLegs ( Path &path, Leg &leg, Leg &leg2, unsigned int legindex, int rightstart, int nodesize2 );
    PatternTree ( PatternTree &parenttree, unsigned int legindex );
    vector<Leg> treetuples;
    vector<NodeId> rightmostindexes;
    vector<short> rootpathrelations;
    unsigned int nextprefixindex;
    unsigned int rootpathstart;
    unsigned int nextpathstart;
    unsigned int maxdepth;
    int symmetric; // 0 == not symmetric, 1 == symmetric, even length path, 2 == symmetric, odd length path
    int secondpathleg;
    vector<Leg> legs; // pointers used to avoid copy-constructor during a resize of the vector
    vector<CloseLeg> closelegs;
    friend ostream &operator<< ( ostream &stream, PatternTree &patterntree );
#ifdef GRAPH_OUTPUT
    friend void fillMatrix ( int **A, int &nextnode, int rootnode, NodeLabel rootlabel, 
                  int startpos, int endpos, PatternTree &patterntree );
    NodeLabel tree1rootlabel, tree2rootlabel;
    EdgeLabel rootpathlabel;
#endif
    TidList *tidlist;
};

#define NONEXTPREFIX ((unsigned int) -1)

#endif
