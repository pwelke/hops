// tidlist.cpp
// Siegfried Nijssen, snijssen@liacs.nl, jul 2004.
#ifndef TIDLIST_H
#define TIDLIST_H
#include "misc.h"

/**
@author Siegfried Nijssen
*/
class TidList{
public:
    TidList();
    
    Tid *tids;
    int tidssize;
    
    void init ( int size ) {
      tids = new Tid[size + 1];
      tids[0] = NOTID; // this flag allows push_back to be more efficient
      tids++;
      tidssize = 0;
    }
    
    void push_back ( Tid tid ) {
      if ( tids[tidssize-1] != tid ) {
        tids[tidssize] = tid;
        tidssize++;
      }
    }
    
    TidList *evaluateState (); 
      // checks the graph in the current graphstate, with all legs stored
      // in the legmanager, returns a list with tids of all graphs that contain
      // the current graphstate. This list manager doesn't maintain the order
      // of tids, and returns a tidlist which stored in the parent that generated
      // it, thus saving memory space

    ~TidList();

};

#endif
