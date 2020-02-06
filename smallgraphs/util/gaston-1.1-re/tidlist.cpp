// tidlist.cpp
// Siegfried Nijssen, snijssen@liacs.nl, jul 2004.
#include "tidlist.h"
#include "database.h"
#include "graphstate.h"
#include "subgraphiso.h"

TidList::TidList()
{
}


TidList::~TidList()
{
}


TidList *TidList::evaluateState () {
  graphstate.subgraphiso->prepare ();
  int front = 0, back = tidssize;
  bool in;
  
  while ( true ) {
    do 
      in = graphstate.subgraphiso->run ( database.trees[tids[front]] );
    while ( in && ++front < back );
    while ( !in && front < --back )
      in = graphstate.subgraphiso->run ( database.trees[tids[back]] );
    if ( front < back ) {
      Tid tid = tids[front];
      tids[front] = tids[back];
      tids[back] = tid;
      front++;
      if ( front >= back )
        break;
    }
    else
      break;
  }
  
  TidList* tidlist = new TidList;
  tidlist->tidssize = front;
  tidlist->tids = tids;
  return tidlist;
}
