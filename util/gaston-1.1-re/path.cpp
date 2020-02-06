// path.cpp
// Siegfried Nijssen, snijssen@liacs.nl, jan 2004.
#include <algorithm>
#include "patterntree.h"
#include "patterngraph.h"
#include "path.h"
#include "graphstate.h"
#include "simplesubiso.h"

Path::Path ( DatabaseEdgeLabel &databaseedgelabel ) {
  NodeLabel startnodelabel = databaseedgelabel.fromnodelabel,
            endnodelabel = databaseedgelabel.tonodelabel;
  EdgeLabel edgelabel = databaseedgelabel.edgelabel;
  
  graphstate.insertStartNode ( startnodelabel );
  graphstate.insertNode ( 0, edgelabel );
  
  OUTPUT(databaseedgelabel.frequency)
  
  frontsymmetry = backsymmetry = 0;
  
  cout << "Edge " 
       << database.nodelabels[startnodelabel].inputlabel << "(" << (int) startnodelabel << ")"
       << "-[" << databaseedgelabel.inputedgelabel << "]-"
       << database.nodelabels[endnodelabel].inputlabel << "(" << (int) endnodelabel << ")" <<endl;
  
  DatabaseNodeLabel &databasenodelabel = database.nodelabels[startnodelabel];
 
  // "trick" to do extensions in two directions: extend one, fill legs for the other  
  
  vector<EdgeLabel> &frequentedgelabels = databasenodelabel.frequentedgelabels;

  for ( int i = 0; i < frequentedgelabels.size (); i++ ) {
    Leg leg;
    leg.depth = 0;
    leg.edgelabel = frequentedgelabels[i];
    leg.connectingnode = 0;
    DatabaseEdgeLabel &databaseedgelabel2 = database.edgelabels[database.edgelabelsindexes[frequentedgelabels[i]]];
    if ( databaseedgelabel2.fromnodelabel == startnodelabel )
      leg.nodelabel = databaseedgelabel2.tonodelabel;
    else
      leg.nodelabel = databaseedgelabel2.fromnodelabel;
    legmanager.appendLeg ( leg );
  }
  nodelabels.push_back ( startnodelabel );
  edgelabels.push_back ( edgelabel );
  nodelabels.push_back ( endnodelabel );
  totalsymmetry = startnodelabel - endnodelabel;
  
  legmanager.appendExtensionLegs ( 1, 1, 0 );

  graphstate.subgraphiso = simplesubiso;
  
  tidlist = databaseedgelabel.tidlist.evaluateState();
  
  legmanager.fillLegs ( legs, closelegs );
}

Path::Path ( Path &parentpath, unsigned int legindex ) {
  Leg &leg = parentpath.legs[legindex];
  int positionshift;
  
  OUTPUT(parentpath.legs[legindex].frequency)
 
  // fill in normalisation information, it seems a lot of code, but in fact it's just a lot
  // of code to efficiently perform one walk through the edge/nodelabels arrays.

  nodelabels.resize ( parentpath.nodelabels.size () + 1 );
  edgelabels.resize ( parentpath.edgelabels.size () + 1 );
  legmanager.appendCloseLegs ( parentpath.closelegs );

  if ( parentpath.nodelabels.size () == 1 ) {
    totalsymmetry = parentpath.nodelabels[0] - leg.nodelabel;
    frontsymmetry = backsymmetry = 0;
    nodelabels[1] = leg.nodelabel;
    edgelabels[0] = leg.edgelabel;
    nodelabels[0] = parentpath.nodelabels[0];
    positionshift = 0;
  }
  else if ( leg.depth == 0 ) {
    positionshift = 1;
    nodelabels[0] = leg.nodelabel;
    edgelabels[0] = leg.edgelabel;

    backsymmetry = parentpath.totalsymmetry;
    frontsymmetry = leg.nodelabel - parentpath.nodelabels[parentpath.nodelabels.size () - 2];
    totalsymmetry = leg.nodelabel - parentpath.nodelabels.back ();
    if ( !totalsymmetry )
      totalsymmetry = leg.edgelabel - parentpath.edgelabels.back ();

    int i = 0;
    // we can prepend only before strings of length 2
    if ( parentpath.nodelabels.size () > 2 ) {
      if ( !frontsymmetry )
        frontsymmetry = leg.edgelabel - parentpath.edgelabels[parentpath.nodelabels.size () - 3];

      while ( !frontsymmetry && i < parentpath.edgelabels.size () / 2 ) {
        nodelabels[i + 1] = parentpath.nodelabels[i];
        edgelabels[i + 1] = parentpath.edgelabels[i];

        frontsymmetry = parentpath.nodelabels[i] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 3];
        if ( !frontsymmetry && parentpath.nodelabels.size () > 3 )
          frontsymmetry = parentpath.edgelabels[i] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 4];

	if ( !totalsymmetry ) {
	  totalsymmetry = parentpath.nodelabels[i] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 2];
	  if ( !totalsymmetry )
	    totalsymmetry = parentpath.edgelabels[i] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 3];
	}

        i++;
      }
    }
    for ( ; !totalsymmetry && i < parentpath.edgelabels.size () / 2; i++ ) {
      nodelabels[i + 1] = parentpath.nodelabels[i];
      edgelabels[i + 1] = parentpath.edgelabels[i];

      totalsymmetry = parentpath.nodelabels[i] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 2];
      if ( !totalsymmetry && parentpath.nodelabels.size () > 3 )
        totalsymmetry = parentpath.edgelabels[i] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 3];
    }
    for ( ;i < parentpath.edgelabels.size (); i++ ) {
      nodelabels[i + 1] = parentpath.nodelabels[i];
      edgelabels[i + 1] = parentpath.edgelabels[i];
    }

    nodelabels[i + 1] = parentpath.nodelabels[i];

    legmanager.appendExtensionLegs ( 0, graphstate.lastNode (), leg.connectingnode );
  }
  else  {
    positionshift = 0;

    frontsymmetry = parentpath.totalsymmetry;
    backsymmetry = parentpath.nodelabels[1] - leg.nodelabel;
    totalsymmetry = parentpath.nodelabels[0] - leg.nodelabel;
    if ( !totalsymmetry )
      totalsymmetry = parentpath.edgelabels[0] - leg.edgelabel;
    int i = 0;
    if ( parentpath.nodelabels.size () > 2 ) {
      if ( !backsymmetry )
        backsymmetry = parentpath.edgelabels[1] - leg.edgelabel;

      while ( !backsymmetry && i < parentpath.edgelabels.size () / 2 ) {
        nodelabels[i] = parentpath.nodelabels[i];
	edgelabels[i] = parentpath.edgelabels[i];

	backsymmetry = parentpath.nodelabels[i + 2] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 1];
	if ( !backsymmetry && parentpath.nodelabels.size () > 3 )
	  backsymmetry = parentpath.edgelabels[i + 2] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 2];

	if ( !totalsymmetry ) {
	  totalsymmetry = parentpath.nodelabels[i + 1] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 1];
	  if ( !totalsymmetry && parentpath.nodelabels.size () > 3 )
	    totalsymmetry = parentpath.edgelabels[i + 1] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 2];
	}
	i++;
      }
    }
    for ( ; !totalsymmetry && i < parentpath.edgelabels.size () / 2; i++ ) {
      nodelabels[i] = parentpath.nodelabels[i];
      edgelabels[i] = parentpath.edgelabels[i];
      totalsymmetry = parentpath.nodelabels[i + 1] - parentpath.nodelabels[parentpath.nodelabels.size () - i - 1];
      if ( !totalsymmetry && i < parentpath.edgelabels.size () - 1 )
        totalsymmetry = parentpath.edgelabels[i + 1] - parentpath.edgelabels[parentpath.nodelabels.size () - i - 2];
    }
    for ( ; i < parentpath.edgelabels.size (); i++ ) {
      nodelabels[i] = parentpath.nodelabels[i];
      edgelabels[i] = parentpath.edgelabels[i];
    }

    nodelabels[i] = parentpath.nodelabels[i];
    edgelabels[i] = leg.edgelabel;
    nodelabels[i+1] = leg.nodelabel;
  }

  int s = parentpath.legs.size ();
  for ( int i = 0; i < s; i++ ) {
    Leg leg2 = parentpath.legs[i];
    leg2.depth += positionshift;
    legmanager.appendLeg ( leg2 );
  }
  
  if ( !positionshift ) 
    legmanager.appendExtensionLegs ( leg.depth + 1, graphstate.lastNode (), leg.connectingnode );
  
  graphstate.subgraphiso = simplesubiso;
  
  tidlist = parentpath.tidlist->evaluateState();
  
  legmanager.fillLegs ( legs, closelegs );  
}

Path::~Path () {
  delete tidlist;
}

// ADDED

extern int counter;

bool Path::isnormal ( EdgeLabel edgelabel ) {
  // symplistic quadratic algorithm
  int nodelabelssize = nodelabels.size (), step, add, start;
  
  edgelabels.push_back ( edgelabel );
    
  // if we would program it better, we would use the 'totalsymmetry' variable here;
  // however, to be quick & easy, we used a different coding here...
  int t = nodelabelssize - 1, r = 0;
  int symmetry;
  do {
    symmetry = nodelabels[t] - nodelabels[r];
    int nt = ( t + nodelabelssize - 1 ) % nodelabelssize;
    if ( !symmetry ) 
      symmetry = edgelabels[nt] - edgelabels[r];
    r = ( r + 1 ) % nodelabelssize;
    t = nt;
  }
  while ( symmetry == 0 && t != nodelabelssize - 1 );
  
  if ( symmetry < 0 ) {
    step = -1 + nodelabelssize ;
    add = -1 + nodelabelssize ;
    start = nodelabelssize - 1;
  }
  else {
    step = 1 + nodelabelssize;
    add = nodelabelssize ;
    start = 0;
  }
  for ( int i = 0; i < nodelabelssize; i++ ) {
    // starting positions for the new path
    int k = start, l = i, p;
    do {
      if ( nodelabels[l] < nodelabels[k] ) {
        edgelabels.pop_back ();
        return false;
      }
      if ( nodelabels[l] > nodelabels[k] )
        break;
      p = ( k + add ) % nodelabelssize;
      l = ( l + nodelabelssize - 1 ) % nodelabelssize;
      if ( edgelabels[l] < edgelabels[p] ) {
        edgelabels.pop_back ();
        return false;
      }
      if ( edgelabels[l] > edgelabels[p] ) 
        break;
      k = ( k + step ) % nodelabelssize;
    }
    while ( k != start );
    
    k = start, l = i;
    do {
      if ( nodelabels[l] < nodelabels[k] ) {
        edgelabels.pop_back ();
        return false;
      }
      if ( nodelabels[l] > nodelabels[k] ) 
        break;
      p = ( k + add ) % nodelabelssize;
      if ( edgelabels[l] < edgelabels[p] ) {
        edgelabels.pop_back ();
        return false;
      }
      if ( edgelabels[l] > edgelabels[p] ) 
        break;
      l = ( l + 1 ) % nodelabelssize;
      k = ( k + step ) % nodelabelssize;
    }
    while ( k != start );
    
  }
  edgelabels.pop_back ();
  return true;
}

void Path::expand2 () {
  // does not work for strings with only one node
  statistics.patternsize++;
  if ( statistics.patternsize > statistics.frequenttreenumbers.size () ) {
    statistics.frequenttreenumbers.push_back ( 0 );
    statistics.frequentpathnumbers.push_back ( 0 );
    statistics.frequentgraphnumbers.push_back ( 0 );
  }
  ++statistics.frequentpathnumbers[statistics.patternsize-1];

  if ( statistics.patternsize == maxsize ) {
    statistics.patternsize--;
    return;
  }
      
  if ( closelegs.size () && phase > 2 ) {
    
    NodeId from = graphstate.nodes.size () - 1;
    NodeId to = 0;
    while ( graphstate.nodes[to].edges.size () == 2 )
      to++;
      
    for ( int i = 0; i < closelegs.size (); i++ ) {
      if ( closelegs[i].from == from &&
           closelegs[i].to == to &&
           isnormal ( closelegs[i].edgelabel ) ) {
        graphstate.insertEdge ( closelegs[i].from, closelegs[i].to, closelegs[i].edgelabel );
        OUTPUT(closelegs[i].frequency)
        int addsize = statistics.patternsize + graphstate.edgessize - graphstate.nodes.size ();
        if ( addsize >= statistics.frequenttreenumbers.size () ) {
          statistics.frequenttreenumbers.resize ( addsize + 1, 0 );
          statistics.frequentpathnumbers.resize ( addsize + 1, 0 );
          statistics.frequentgraphnumbers.resize ( addsize + 1, 0 );
        }
        statistics.frequentgraphnumbers[addsize]++;
        graphstate.deleteEdge ( closelegs[i].from, closelegs[i].to );
        
        // DON'T RECURSE GRAPH GROWING!
        // only circle graphs can only grow from paths, all other graphs
        // can grow from spanning trees, which we prefer for now
      }
    }
  }

  for ( int i = 0; i < legs.size (); i++ ) {
    Leg &tuple = legs[i];
    if ( tuple.depth == nodelabels.size () - 1 ) {
      if ( tuple.nodelabel > nodelabels[0] ||
           ( tuple.nodelabel == nodelabels[0] &&
             ( tuple.edgelabel > edgelabels[0] ||
               ( tuple.edgelabel == edgelabels[0] && backsymmetry <= 0 )
             )
           ) ) {
        graphstate.insertNode ( tuple.connectingnode, tuple.edgelabel );
        Path path ( *this, i );
        path.expand2 ();
	graphstate.deleteNode ();
      }
    }
    else
      if ( tuple.depth == 0 ) {
        if ( totalsymmetry &&
             ( tuple.nodelabel > nodelabels.back () ||
             ( tuple.nodelabel == nodelabels.back () &&
               ( tuple.edgelabel > edgelabels.back () ||
                 ( tuple.edgelabel == edgelabels.back () && frontsymmetry >= 0 )
               )
             ) ) ) {
          graphstate.insertNode ( tuple.connectingnode, tuple.edgelabel );
          Path path ( *this, i );
          path.expand2 ();
	  graphstate.deleteNode ();
        }
      }
      else {
        if ( ( totalsymmetry || tuple.depth <= edgelabels.size () / 2 ) &&
	     ( tuple.depth != 1 || tuple.edgelabel >= edgelabels[0] ) &&
	     ( tuple.depth != nodelabels.size () - 2 || tuple.edgelabel >= edgelabels.back () ) &&
	     phase > 1
	   ) {
          graphstate.insertNode ( tuple.connectingnode, tuple.edgelabel );
	  PatternTree tree ( *this, i );
	  tree.expand ();
	  graphstate.deleteNode ();
	 // grow tree
        }
      }
  }

  statistics.patternsize--;
}

void Path::expand () {
  expand2 ();
  graphstate.deleteNode ();
  graphstate.deleteStartNode ();
}

ostream &operator<< ( ostream &stream, Path &path ) {
  stream << database.nodelabels[path.nodelabels[0]].inputlabel;
  for ( int i = 0; i < path.edgelabels.size (); i++ ) {
    //stream << (char) ( path.edgelabels[i] + 'A' ) << path.nodelabels[i+1];
    stream << database.edgelabels[database.edgelabelsindexes[path.edgelabels[i]]].inputedgelabel << database.nodelabels[path.nodelabels[i+1]].inputlabel;
  }
  return stream;
}
