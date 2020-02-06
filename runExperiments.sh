#!/bin/env bash

## To run the frequent pattern mining experiments reported in the paper, just run this file. 
## In each output folder, there will be tex files that can be compiled to show the plots.


# requirements: gnu-parallel 
# sudo apt install parallel


## Parameters of the experiment can be set by exporting the variables below.
## Our experiments use standard values for all parameters, except the one changing for the datasets.
# export exp=
# export outputfolder=
# export relthreshold= 
# export maxpatternsize=
# export repetitions=
# export embOps=
# export ks=
# export nparalleljobs=
# export experimenttimeout=
# export datasets=

export outputfolder=./chemical
bash ProbabilisticPatternMiningExperiment.sh

export outputfolder=./threshold
bash ProbabilisticPatternMiningExperiment.sh

export outputfolder=./random
bash ProbabilisticPatternMiningExperiment.sh

export outputfolder=./social
bash ProbabilisticPatternMiningExperiment.sh

bash plotResults.sh
