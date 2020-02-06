//
// C++ Interface: legmanager
//
// Description: 
//
//
// Author: Siegfried Nijssen <snijssen@snijssen@liacs.nl>, (C) 2004
//
// Copyright: See COPYING file that comes with this distribution
//
//
#ifndef LEGMANAGER_H
#define LEGMANAGER_H
#include "misc.h"
#include "subgraphiso.h"

/**
@author Siegfried Nijssen
*/

// legs are stored with the structures in the recursive search

struct Leg {
  NodeId connectingnode;
  Depth depth;
  NodeLabel nodelabel;
  EdgeLabel edgelabel;
  Frequency frequency;
  friend bool operator< ( Leg &a, Leg &b ) { return a.depth > b.depth || ( a.depth == b.depth && a.edgelabel < b.edgelabel ); }
  friend bool operator== ( Leg &a, Leg &b ) { return a.depth == b.depth && a.edgelabel == b.edgelabel; }
};

struct CloseLeg {
  NodeId from, to;
  EdgeLabel edgelabel;
  Frequency frequency;
  friend bool operator< ( const CloseLeg &a, const CloseLeg &b ) { return a.from < b.from || ( a.from == b.from && ( a.to < b.to || ( a.to == b.to && a.edgelabel < b.edgelabel ) ) ); }
  friend bool operator> ( const CloseLeg &a, const CloseLeg &b ) { return a.from > b.from || ( a.from == b.from && ( a.to > b.to || ( a.to == b.to && a.edgelabel > b.edgelabel ) ) ); }
};

// eval legs are used internally by the leg manager

struct CountEvalLeg {
  Frequency frequency;
  Tid lasttid;
  bool setactivated;
  CountEvalLeg (): frequency ( 0 ), lasttid ( NOTID ), setactivated ( false ) { }
};

struct CloseEvalLeg {
  CountEvalLeg *countleg;
  NodeId tonode; // node with which to close
};

struct LabelEvalLeg {
  CountEvalLeg countleg; // (node,label) pair extension with new node
  vector<CloseEvalLeg> closelegs; 
    // closing legs, we assume there are few so we treat these less efficiently
};

struct NodeEvalLeg {
  int nsetactivatedlegs;
  LabelEvalLeg *labellegs;
};

class LegManager{
  private:
    int nlabels;
    NodeEvalLeg *nodelegs;
    int *nactivelegs; 
      // we could have put these into the NodeEvalLeg, but we choose to save one 
      // dereference step.
    DatabaseTree *curdatabasetree;
    
    vector<Leg> legs;
    vector<CloseLeg> closelegs;
    
    NodeId extensionconnectingnode, extensionparentnode;
    Depth extensiondepth;
    EdgeLabel extensionminlabel, extensionexceptionlabel, extensionneglectlabel;
    int extensionlegspos;
    void fillExtensionLeg ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs, LabelEvalLeg &labelleg, NodeId nodeid, EdgeLabel edgelabel );
    void fillExtensionLegs ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs );
    void processNewOccurrenceExtension ( SubGraphIso *subgraphiso );
    int *secondpathmarker;
    int secondpathpos;
    bool secondpathsec; // secondpathsec == true iff secondpath set after extensionpos
  public:
    LegManager();
    
    // should be optimised away by the compiler
    inline bool isActive ( NodeId nodeid ) const {
      return nactivelegs[nodeid];
    }

    ~LegManager();
    void init ( int maxnodes, int nlabels );
    
    // to be called each time before a new transaction is processed
    void setNewDatabaseGraph ( DatabaseTree *databasetree );
    
    // to be called after all legs have been counted
    // Note: uses the current graphstate to fill in target nodelabels
    void fillLegs ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs );
    
    // to be called when a non-closing leg must be counted
    void appendLeg ( Leg &leg );
    
    // to be called when a closing leg must be counted
    void appendCloseLeg ( CloseLeg &leg ); 
    
    void appendCloseLegs ( vector<CloseLeg> &closelegs );
    
    // set the extension node, including the minimal label and the
    // exception minimum label
    void appendExtensionLegs ( Depth depth, NodeId connectingnode, NodeId parentnode, EdgeLabel minlabel = MINEDGELABEL, EdgeLabel exceptionlabel = NOEDGELABEL, EdgeLabel neglectlabel = NOEDGELABEL );
    
    void appendSecondPathMarker ( int &marker );
        
    // to be called each time that for the current database graph
    // a new occurrence is found. Uses datastructures of the subgraphiso algorithm 
    void processNewOccurrence ( SubGraphIso *subgraphiso );
    
};

extern LegManager legmanager;

#endif
