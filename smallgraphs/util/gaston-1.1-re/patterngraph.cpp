// patterngraph.cpp
// Siegfried Nijssen, snijssen@liacs.nl, jan 2004.
#include "patterngraph.h"
#include "graphstate.h"
#include "simplesubiso.h"

vector<Leg> dummylegs; // should not be used

void PatternGraph::init ( vector<CloseLeg> &closelegssource, int legindex, TidList *ptidlist ) {
  closetuples.push_back ( closelegssource[legindex] );
  frequency = closelegssource[legindex].frequency;
  this->closelegssource = &closelegssource;
  this->ptidlist = ptidlist;
  this->legindex = legindex;
  // ADDED
  graphstate.closetuples = &closetuples;
}

void PatternGraph::expand () {
  int id = graphstate.isnormal ();
  if ( id == 0 ) {
    OUTPUT(frequency)
    int addsize = statistics.patternsize + graphstate.edgessize - graphstate.nodes.size ();
    if ( addsize >= statistics.frequenttreenumbers.size () ) {
      statistics.frequenttreenumbers.resize ( addsize + 1, 0 );
      statistics.frequentpathnumbers.resize ( addsize + 1, 0 );
      statistics.frequentgraphnumbers.resize ( addsize + 1, 0 );
    }
    statistics.frequentgraphnumbers[addsize]++;
    if ( closelegssource->size () == legindex + 1 ) {
      tidlist = NULL;
      // no need to go through the database
      return;
    }
    
    for ( int k = legindex + 1; k < closelegssource->size (); k++ ) 
      legmanager.appendCloseLeg ( (*closelegssource)[k] );

    graphstate.subgraphiso = simplesubiso;
  
    tidlist = ptidlist->evaluateState();
      
    legmanager.fillLegs ( dummylegs, closelegs );
    
    //cout << graphstate << endl;
  for ( int k = 0; k < closelegs.size (); k++ ) {
    graphstate.insertEdge ( closelegs[k].from, closelegs[k].to, closelegs[k].edgelabel );
    PatternGraph patterngraph ( *this, k );
    patterngraph.expand ();
    graphstate.deleteEdge ( closelegs[k].from, closelegs[k].to );
  }
  }
  else tidlist = NULL;
}

PatternGraph::~PatternGraph () {
  if ( tidlist )
    delete tidlist;
}
