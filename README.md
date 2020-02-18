# HOPS
Code and data for an anonymous KDD submission

You can find the code for experiments and plot generation of Section 6.1: Approximate Counting in Large Graphs in the /largegraph/ folder.
The code for experiments and plot generation of Section 6.2: Probabilistic Frequent Subtree Mining is located in the /smallgraphs/ folder.

The code has been tested on recent Ubuntu Linux distributions (18.04, 19.10).

# How To Run Approximate Counting Experiments on Large Graphs

Set up the experiments and evaluation:
1. Clone the project
2. Set up python3 conda environment for hops:
   * conda create -n hops python=3.7 joblib matplotlib
   * pip install tikzplotlib
3. Set up python2 for Ravkic algorithms:
   * install python2.7: sudo apt install python2.7 python-pip
   * sudo apt-get install python-tk

4. Set up experiments:
   * in **run_exp.py** set *main_path=".../largegraph"*
   * run **run_exp.py** with your favourite graph, pattern size and time limit
5. Set up evaluation:
   * in **evaluate.py** set *path=".../largegraph/*
   * run **evaluate.py** for evaluation 

# How To Run Probabilistic Subtree Mining Experiments on Small Graphs

1. (Clone the project)
2. Install gnu parallel: **sudo apt install parallel**
3. Run **smallgraphs/runExperiments.sh**
4. Inspect results in the subfolders
