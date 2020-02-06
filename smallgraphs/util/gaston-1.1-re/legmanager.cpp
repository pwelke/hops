//
// C++ Implementation: legmanager
//
// Description: 
//
//
// Author: Siegfried Nijssen <snijssen@snijssen@liacs.nl>, (C) 2004
//
// Copyright: See COPYING file that comes with this distribution
//
//
#include "legmanager.h"
#include "graphstate.h"
#include <algorithm> 

LegManager legmanager;

LegManager::LegManager() {
  extensionlegspos = -1;
  secondpathpos = -1;
  secondpathsec = false;
}


LegManager::~LegManager() {
}

void LegManager::init ( int maxnodes, int nlabels ) {
  nodelegs = new NodeEvalLeg[maxnodes];
  nactivelegs = new int[maxnodes];
  this->nlabels = nlabels;
  for ( int i = 0; i < maxnodes; i++ ) {
    nactivelegs[i] = 0;
    nodelegs[i].labellegs = new LabelEvalLeg[nlabels];
  }
}

void LegManager::setNewDatabaseGraph ( DatabaseTree *databasetree ) {
  NodeId nodeid;
  int size = graphstate.nodes.size ();
  for ( int i = 0; i < size; i++ ) {
    nactivelegs[i] = nodelegs[i].nsetactivatedlegs;
  }
  curdatabasetree = databasetree;
}

void LegManager::fillExtensionLeg ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs, LabelEvalLeg &labelleg, NodeId nodeid, EdgeLabel edgelabel ) {
  if ( edgelabel != extensionneglectlabel && 
       edgelabel >= extensionminlabel && labelleg.countleg.frequency >= minfreq ) {
    Leg leg;
    leg.connectingnode = nodeid;
    leg.depth = extensiondepth;
    leg.edgelabel = edgelabel;
    DatabaseEdgeLabel &dataedgelabel = database.edgelabels[database.edgelabelsindexes[edgelabel]];
    if ( dataedgelabel.fromnodelabel == graphstate.nodes[nodeid].label )
      leg.nodelabel = dataedgelabel.tonodelabel;
    else
      leg.nodelabel = dataedgelabel.fromnodelabel;
    leg.frequency = labelleg.countleg.frequency;
    targetlegs.push_back ( leg );
  }
  
  int s = labelleg.closelegs.size ();
  for ( int i = 0; i < s; i++ ) {
    if ( labelleg.closelegs[i].countleg->frequency >= minfreq ) {
      CloseLeg closeleg;
      closeleg.edgelabel = edgelabel;
      closeleg.from = nodeid;
      closeleg.to = labelleg.closelegs[i].tonode;
      closeleg.frequency = labelleg.closelegs[i].countleg->frequency;
      delete labelleg.closelegs[i].countleg; 
      targetcloselegs.push_back ( closeleg );
    }
  }
  labelleg.countleg = CountEvalLeg ();
  labelleg.closelegs.resize ( 0 );
}


void LegManager::fillExtensionLegs ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs ) {
  nodelegs[extensionconnectingnode].nsetactivatedlegs = 0;
  if ( extensionexceptionlabel != NOEDGELABEL ) 
    fillExtensionLeg ( targetlegs, targetcloselegs, nodelegs[extensionconnectingnode].labellegs[extensionexceptionlabel], extensionconnectingnode, extensionexceptionlabel );
  for ( int i = 0; i < nlabels; i++ )
    if ( i != extensionexceptionlabel )
      fillExtensionLeg ( targetlegs, targetcloselegs, nodelegs[extensionconnectingnode].labellegs[i], extensionconnectingnode, i );
      
  std::sort ( targetcloselegs.begin (), targetcloselegs.end () );
}

// to be called to fill in the refinements found
void LegManager::fillLegs ( vector<Leg> &targetlegs, vector<CloseLeg> &targetcloselegs ) {
  // copy the data in the current active legs datastructures to the
  // paramater legs, clean up the information as it has been copied
  
  // first the old closing legs
  int s = closelegs.size ();
  for ( int i = 0; i < s; i++ ) {
    NodeId tonode = closelegs[i].to;
    vector<CloseEvalLeg> &closeevallegs = nodelegs[closelegs[i].from].labellegs[closelegs[i].edgelabel].closelegs;
    nodelegs[closelegs[i].from].nsetactivatedlegs = 0;
    int s2 = closeevallegs.size ();
    for ( int j = 0; j < s2; j++ ) {
      if ( closeevallegs[j].tonode == tonode && closeevallegs[j].countleg->frequency >= minfreq ) {
        closelegs[i].frequency = closeevallegs[j].countleg->frequency;
        delete closeevallegs[j].countleg;
        targetcloselegs.push_back ( closelegs[i] );
      }
    }
 }
  
  // disable all closing legs that were set (may set the size of one entry
  // multiple times to zero --- could therefore perhaps be done more efficiently
  // The question is however whether doing it more efficiently doesn't just 
  // take more time than just doing it
  for ( int i = 0; i < s; i++ ) {
    nodelegs[closelegs[i].from].labellegs[closelegs[i].edgelabel].closelegs.resize ( 0 );
    nodelegs[closelegs[i].to].labellegs[closelegs[i].edgelabel].closelegs.resize ( 0 );
  }
  
  // now the old normal legs, mixed with the extension legs
  
  s = legs.size ();
  for ( int i = 0; i <= s; i++ ) {
    if ( i == secondpathpos )
      *secondpathmarker = targetlegs.size ();
    if ( i == extensionlegspos ) {
      fillExtensionLegs ( targetlegs, targetcloselegs );
      if ( i == secondpathpos && secondpathsec )  
         // secondpathsec == true if secondpathpos was set after the extensionlegpos
        *secondpathmarker = targetlegs.size ();
    }
    if ( i < s ) {
      CountEvalLeg &countleg = nodelegs[legs[i].connectingnode].labellegs[legs[i].edgelabel].countleg;
      nodelegs[legs[i].connectingnode].nsetactivatedlegs = 0;
      if ( countleg.frequency >= minfreq ) {
        legs[i].frequency = countleg.frequency;
        targetlegs.push_back ( legs[i] );
      }
      countleg = CountEvalLeg ();
    }
  }
  
  closelegs.resize ( 0 );
    // we used this array to store the countevallegs for closing legs; as these are
    // treated symmetrically, we choose to store these with neither of the two entries
    // in the array
  legs.resize ( 0 );
  
  extensionlegspos = -1;
  secondpathpos = -1;
  secondpathsec = false;
}

// to be called when a non-closing leg must be counted
void LegManager::appendLeg ( Leg &leg ) {
  nodelegs[leg.connectingnode].labellegs[leg.edgelabel].countleg.setactivated = true;
  nodelegs[leg.connectingnode].nsetactivatedlegs++;
  legs.push_back ( leg );
}

// to be called when a closing leg must be counted
void LegManager::appendCloseLeg ( CloseLeg &leg ) {
  CloseEvalLeg closeevalleg;
  closeevalleg.countleg = new CountEvalLeg;
  closeevalleg.countleg->setactivated = true;
  
  // closing extensions are treated symmetrically
  closeevalleg.tonode = leg.to;
  nodelegs[leg.from].labellegs[leg.edgelabel].closelegs.push_back ( closeevalleg );
  nodelegs[leg.from].nsetactivatedlegs++;
  
  closeevalleg.tonode = leg.from;
  nodelegs[leg.to].labellegs[leg.edgelabel].closelegs.push_back ( closeevalleg );
  nodelegs[leg.to].nsetactivatedlegs++;
  closelegs.push_back ( leg );
}

void LegManager::appendCloseLegs ( vector<CloseLeg> &legs ) {
  int s = legs.size ();
  for ( int i = 0; i < s; i++ )
    appendCloseLeg ( legs[i] );
}

// set the extension node, including the minimal label and the
// exception minimum label
void LegManager::appendExtensionLegs ( Depth depth, NodeId connectingnode, NodeId parentnode, EdgeLabel minlabel, EdgeLabel exceptionlabel, EdgeLabel neglectlabel ) {
  extensionconnectingnode = connectingnode;
  extensiondepth = depth;
  extensionexceptionlabel = exceptionlabel;
  extensionlegspos = legs.size ();
  extensionminlabel = minlabel;
  extensionparentnode = parentnode;
  extensionneglectlabel = neglectlabel;
  nodelegs[connectingnode].nsetactivatedlegs = 0; 
    // we will always count the extension leg
  secondpathsec = false;
}

void LegManager::processNewOccurrenceExtension ( SubGraphIso *subgraphiso ) {
  DatabaseTreeNode &dtn = subgraphiso->databasetree->nodes[
      subgraphiso->map[extensionconnectingnode] ];
  Tid tid = subgraphiso->databasetree->tid;
    
  int s = dtn.edges.size ();
  NodeId tonode;
  EdgeLabel edgelabel;
  for ( int i = 0; i < s; i++ ) {
    tonode = dtn.edges[i].tonode;
    edgelabel = dtn.edges[i].edgelabel;
    LabelEvalLeg &leg = nodelegs[extensionconnectingnode].labellegs[edgelabel];
    // may count the exception label too
    if ( subgraphiso->used[tonode] ) {
      NodeId usedbynode = subgraphiso->used[tonode] - 1;
      if ( usedbynode != extensionparentnode ) {
        // real cycle found, search to count, for the moment simple linear search
        int s2 = leg.closelegs.size ();
        int k = 0;
        while ( k < s2 && leg.closelegs[k].tonode < usedbynode )
          k++;
        if ( k < s2 && leg.closelegs[k].tonode == usedbynode ) {
          if ( leg.closelegs[k].countleg->lasttid != tid ) {
            leg.closelegs[k].countleg->lasttid = tid;
            leg.closelegs[k].countleg->frequency++;
          }
          //break;
        }
        else {
          CloseEvalLeg closeevalleg;
          closeevalleg.countleg = new CountEvalLeg;
          closeevalleg.countleg->setactivated = true;
          closeevalleg.countleg->frequency = 1;
          closeevalleg.countleg->lasttid = tid;
          closeevalleg.tonode = usedbynode;
          leg.closelegs.insert ( leg.closelegs.begin () + k, closeevalleg );
        }
      }
    }
    else {
      if ( edgelabel >= extensionminlabel && leg.countleg.lasttid != tid ) {
        leg.countleg.lasttid = tid;
        leg.countleg.frequency++;
      }
    }
  }
}

// to be called each time that for the current database graph
// a new occurrence is found. Uses datastructures of the subgraphiso algorithm 
void LegManager::processNewOccurrence ( SubGraphIso *subgraphiso ) {
  vector<NodeId> &changednodes = subgraphiso->changednodes;
  int *used = subgraphiso->used;
  int size = changednodes.size ();
  Tid tid = subgraphiso->databasetree->tid;
  
  if ( extensionlegspos != -1 )
    processNewOccurrenceExtension ( subgraphiso );
      
  for ( int i = 0; i < size; i++ ) {
    NodeId datanode = changednodes[i];
    if ( !isActive ( changednodes[i] ) )
      continue;
    DatabaseTreeNode &dtn = subgraphiso->databasetree->nodes[
        subgraphiso->map[datanode] ];
    int s = dtn.edges.size ();
    NodeId tonode;
    EdgeLabel edgelabel;
    for ( int j = 0; j < s; j++ ) {
      tonode = dtn.edges[j].tonode;
      edgelabel = dtn.edges[j].edgelabel;
      LabelEvalLeg &leg = nodelegs[datanode].labellegs[edgelabel];
      if ( used[tonode] ) {
        if ( !leg.closelegs.empty () ) {
          // check whether this extion is to be counted
          int s2 = leg.closelegs.size ();
          NodeId ptonode = used[tonode] - 1;
          for ( int k = 0; k < s2; k++ )
            if ( leg.closelegs[k].tonode == ptonode ) {
              if ( leg.closelegs[k].countleg->lasttid != tid ) {
                leg.closelegs[k].countleg->frequency++;
                leg.closelegs[k].countleg->lasttid = tid;
                nactivelegs[datanode]--;
                nactivelegs[leg.closelegs[k].tonode]--; 
                  // symmetric, countleg is in both arrays
              }
              break;
            }              
        }
      }
      else {
        if ( leg.countleg.setactivated ) {
          Tid tid = subgraphiso->databasetree->tid;
          if ( leg.countleg.lasttid != tid ) {
            leg.countleg.frequency++;
            leg.countleg.lasttid = tid;
            nactivelegs[datanode]--; 
              // we have found an occurrence for this leg, we don't
              // have to check it further.
          }
        }
      }
    }
  }
}

void LegManager::appendSecondPathMarker ( int &marker ) {
  secondpathmarker = &marker;
  secondpathpos = legs.size ();
  secondpathsec = true;
}
