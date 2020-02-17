# HOPS
Code and data for an anonymous KDD submission

You can find the code for experiments and plot generation of Section 6.1: Approximate Counting in Large Graphs in the /largegraph/ folder.
The code for experiments and plot generation of Section 6.2: Probabilistic Frequent Subtree Mining is located in the /smallgraphs/ folder.

The code has been tested on recent Ubuntu Linux distributions (18.04, 19.10).

# How To Run Approximate Counting Experiments on Large Graphs

Set up the experiments and evaluation:
1. Clone the project
2. Unzip **data_ravkic.zip** to your favourite folder *.../YourFolder*
3. Set up experiments:
   * in **run_exp.py** set *main_path=".../YourFolder"*
   * create an folder for output *.../YourOutputFolder*
   * in **run_exp.py** set *main_out_path=".../YourOutputFolder"*
   * run **run_exp.py** with your favourite graph, pattern size and time limit
4. Set up evaluation:
   * in **evaluate.py** set *path=".../YourOutputFolder*
   * run **evaluate.py** for evaluation 

# How To Run Probabilistic Subtree Mining Experiments on Small Graphs

1. (Clone the project)
2. Install gnu parallel: **sudo apt install parallel**
3. Run **smallgraphs/runExperiments.sh**
4. Inspect results in the subfolders
