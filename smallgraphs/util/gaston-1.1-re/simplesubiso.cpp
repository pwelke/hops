// simplesubiso.cpp
// Siegfried Nijssen, snijssen@liacs.nl, jul 2004.
#include "simplesubiso.h"
#include "graphstate.h"
#include "legmanager.h"
#include <queue>
#include <cstring>

PATMASKTYPE mask[MAXPATSIZE]; 
  // for the moment restricted to patterns with maximum size 32


SimpleSubIso *simplesubiso;

bool SimpleSubIso::isEdge ( NodeId node1, NodeId node2, EdgeLabel label ) {
  int s = databasetree->nodes[node1].edges.size ();
  for ( int i = 0; i < s; i++ )
    if ( databasetree->nodes[node1].edges[i].tonode == node2 &&
         databasetree->nodes[node1].edges[i].edgelabel == label )
      return true;
  return false;
}

// this function is extremely critical!
void SimpleSubIso::recurse ( int acti, int tonode, int d ) {
  NodeId connectto = g1actions[acti].connectto;
  map[connectto] = tonode;
  bool isactive = legmanager.isActive ( connectto );
  if ( isactive )
    changednodes.push_back ( connectto );
  bttomark.push_back ( tonode );
  used[tonode] = connectto + 1;
  bool stop = true;
  if ( d < btdepth )
    btdepth = d;
  
  do
    acti++;
  while ( acti < g1actionssize &&
          g1actions[acti].close && 
          ( stop = isEdge ( map[g1actions[acti].connectfrom], 
                            map[g1actions[acti].connectto], 
                            g1actions[acti].edgelabel ) ) );
  if ( !stop ) {
    used[tonode] = 0;
    bttomark.pop_back ();
    if ( isactive )
      changednodes.pop_back ();
    return;
  }
  
  if ( acti == g1actionssize ) {
    legmanager.processNewOccurrence ( this );

    found = true;
    for ( int i = btdepth; i < g1size; i++ ) 
      databasetree->nodes[bttomark[i]].mark |= usemark;
    databasetree->nodes[bttomark[0]].startmark |= usemark;
    btdepth = g1size;
        //changednodes.resize ( 0 );
    used[tonode] = 0;
    bttomark.pop_back ();
    if ( isactive )
      changednodes.pop_back ();
    return;
  }
  
  NodeId node = map[g1actions[acti].connectfrom], node2;
  EdgeLabel label = g1actions[acti].edgelabel;
  DatabaseTreeNode &dtn = databasetree->nodes[node];
  int s = dtn.edges.size ();
  NodeId id = g1actions[acti].connectto;
  
  if ( id == lastnode ) {
    for ( int i = 0; i < s; i++ ) {
      register DatabaseTreeEdge &edge = dtn.edges[i];
      node2 = edge.tonode;
      if ( edge.edgelabel == label && !used[node2] )
        recurse ( acti, node2, d + 1 );
    }
  }
  else {
    for ( int i = 0; i < s; i++ ) {
      register DatabaseTreeEdge &edge = dtn.edges[i];
      node2 = edge.tonode;
      if ( edge.edgelabel == label && !used[node2] && 
           ( ( databasetree->nodes[node2].mark & usedmark ) ) ) // & mask[id] ) == mask[id] ) )
        recurse ( acti, node2, d + 1 );
    }
  }
  
  used[tonode] = 0;
  bttomark.pop_back ();
  if ( isactive && !changednodes.empty () )
    changednodes.pop_back ();
}

SimpleSubIso::SimpleSubIso () {
  startnodes[0] = 1;
}

SimpleSubIso::~SimpleSubIso() {
  delete[] map;
  delete[] temp;
  delete[] used;
}

void SimpleSubIso::init( int maxnredges, int maxnrnodes ) {
  map = new int[maxnrnodes];
  temp = new int[maxnrnodes];
  used = new int[maxnrnodes];
  g1actions = new Action[maxnredges + maxnrnodes + 1];
}

struct PriorityAction {
  SimpleSubIso::Action action;
  int labelocc;
  int degree;
  int condegree;
};

bool operator< ( const PriorityAction &p1, const PriorityAction &p2 ) {
  return p1.labelocc > p2.labelocc ||
         ( p1.labelocc == p2.labelocc &&
	   p1.condegree < p2.condegree ||
	   ( p1.condegree == p2.condegree &&
	     p1.degree < p2.degree 
	   )
	 );
}

void SimpleSubIso::prepare () {
  g1size = graphstate.nodes.size ();
  bool used2[g1size];
  bool added[g1size];
  NodeId node, node2;
  int s;
  memset ( used2, 0, g1size * sizeof ( bool ) );
  memset ( added, 0, g1size * sizeof ( bool ) );
  
  lastnode = graphstate.nodes.size () - 1;
  usedmark = ( (PATMASKTYPE) 1 ) << ( graphstate.edgessize - 1 );
  usemark = ( (PATMASKTYPE) 1 ) << graphstate.edgessize;
  
  /*unsigned int m = ( 1 << ( graphstate.edgessize ) ) - 1;
  for ( int i = 0; i < g1size; i++ )
    mask[i] = ( ~( ( 1 << i ) - 1 ) ) & m;*/

/*  cout << "USEDMARK: " << usedmark << " " << (int) lastnode << endl
       << "USEMARK: " << usemark << " " << ( graphstate.nodes.size () - 1 ) << endl;*/
  
  static priority_queue<PriorityAction> queue;
  PriorityAction pa;
  
  // find the "most difficult" node first (using occcounts as heuristics)
  NodeLabel startlabel = graphstate.nodes[0].label;
  Frequency startlabelocc = database.nodelabels[startlabel].occcount;
  int degree = graphstate.nodes[0].edges.size ();
  NodeId startnode = 0;
  Frequency occ;
  for ( int i = 1; i < g1size; i++ ) {
    occ = database.nodelabels[graphstate.nodes[i].label].occcount;
    if ( occ < startlabelocc ) {
      startlabelocc = occ;
      startlabel = graphstate.nodes[i].label;
      degree = graphstate.nodes[i].edges.size ();
      startnode = i;
    }
    /* else
      if ( occ == startlabelocc && graphstate.nodes[i].edges.size () > degree ) {
        degree = graphstate.nodes[i].edges.size ();
	startnode = i;
      }*/
  }
  
  pa.action.close = false;
  pa.action.connectfrom = NONODE;
  pa.action.connectto = startnode;
  pa.action.edgelabel = startlabel; // not fair completely

  used2[startnode] = true;
  startnodes[graphstate.edgessize] = startnode;
  
  queue.push ( pa );
  g1actionssize = 0;
  
  while ( !queue.empty () ) {
    PriorityAction pa2 = queue.top ();
    queue.pop ();
    g1actions[g1actionssize++] = pa2.action;
    added[pa2.action.connectto] = true;
    node = pa2.action.connectto;
    s = graphstate.nodes[node].edges.size ();
    for ( int i = 0; i < s; i++ ) {
      node2 = graphstate.nodes[node].edges[i].tonode;
      if ( node2 == pa2.action.connectfrom )
	continue;
      pa.action.close = used2[node2];
      pa.action.connectfrom = node;
      pa.action.connectto = node2;
      pa.action.edgelabel = graphstate.nodes[node].edges[i].edgelabel;
      if ( pa.action.close ) {
        if ( added[node2] )
	  g1actions[g1actionssize++] = pa.action;
      }
      else {
        pa.labelocc = database.nodelabels[graphstate.nodes[node2].label].occcount;
        pa.degree = graphstate.nodes[node2].edges.size ();
        pa.condegree = graphstate.nodes[node].edges.size ();
	queue.push ( pa );
        used2[node2] = true;
      }
    }
  }
}

bool SimpleSubIso::run ( DatabaseTree *databasetree ) {
  legmanager.setNewDatabaseGraph ( databasetree );
  this->databasetree = databasetree;
  g2size = databasetree->nodes.size ();
  found = false;
  int start;
  for ( int i = 0; i < g2size; i++ ) {
    databasetree->nodes[i].mark &= ~usemark;
    databasetree->nodes[i].startmark &= ~usemark;
    used[i] = 0;
  }
  changednodes.resize ( 0 );
  bttomark.resize ( 0 );
  btdepth = 0;
  
  if ( startnodes[graphstate.edgessize - 1] == startnodes[graphstate.edgessize] )
    for ( int k = 0; k < g2size; k++ ) {
      if ( ( databasetree->nodes[k].startmark & usedmark ) && 
           g1actions[0].edgelabel == databasetree->nodes[k].nodelabel ) {
        recurse ( 0, k, 0 );
      }
    }
  else
    for ( int k = 0; k < g2size; k++ )
      if ( g1actions[0].edgelabel == databasetree->nodes[k].nodelabel ) {
        recurse ( 0, k, 0 );
      }
      
  return found;
}
