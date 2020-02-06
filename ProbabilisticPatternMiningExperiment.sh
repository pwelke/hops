#!/bin/env bash

echo ---- BEGIN PARAMETERS ----
echo You can set them by defining and exporting them in your shell
echo

exp=${exp:-'./util'}
echo Experiments folder: 
echo exp = ${exp}
echo

outputfolder=${outputfolder:-'chemical'}
echo Output folder: 
echo outputfolder = ${outputfolder}
echo

relthreshold=${relthreshold:-2}
echo Relative frequency threshold: 
echo relthreshold = ${relthreshold} \%
echo

maxpatternsize=${maxpatternsize:-10}
echo Maximum Pattern Size: 
echo maxpatternsize = ${maxpatternsize}
echo

repetitions=${repetitions:-`seq 1 10`}
echo Repetitions of each experiment: 
echo repetitions = ${repetitions}
echo

embOps=${embOps:-'ps bps hops'}
echo Embedding Operators: 
echo embOps = ${embOps}
echo

ks=${ks:-`seq 1 1 10` `seq 20 10 100` `seq 200 100 1000` `seq 2000 2000 20000`}
echo Sampling Parameters: 
echo ks = ${ks}
echo

nparalleljobs=${nparalleljobs:-4}
echo Number of Parallel Jobs: 
echo nparalleljobs = ${nparalleljobs}
echo

experimenttimeout=${experimenttimeout:-21600}
echo Stop adding runs after X seconds:
echo experimenttimeout = ${experimenttimeout}
echo

echo We consider the following datasets:
datasets=${datasets:-`ls ${outputfolder}/*.txt`}
echo datasets = ${datasets}

echo ---- END OF PARAMETERS ----
echo
echo


## DO ACTUAL STUFF

echo Create output folders...
for embOp in ${embOps}; do
    mkdir ${outputfolder}/${embOp}
done

for outputName in ${embOps}; do
    echo Start processing ${outputName} embedding operator
    
    for dataset in ${datasets}; do
        echo ...for ${dataset}

        # we want to give a fixed time limit for each embedding operator and each dataset
        starttime=$(date +%s)

        # transform parameters
        dataset=`basename ${dataset}`
        threshold=`${exp}/rel2absThreshold ${relthreshold} ${outputfolder}/${dataset}`

        for k in ${ks}; do 
            for run in ${repetitions}; do

                # if time is not yet up, run the next experiment
                currenttime=$(date +%s)
                elapsedtime=$(($currenttime - $starttime)) 
                if [ $elapsedtime -lt $experimenttimeout ] ; then
                
                    sem --id blub --max-procs ${nparalleljobs} \
                      /usr/bin/time \
                        --format="${outputName}\ ${dataset}\ %U" \
                        --output=${outputfolder}/${outputName}/${dataset}_k${k}_run${run}.time \
                      ${exp}/bin/lwg \
                        -i ${k} \
                        -e ${outputName} \
                        -p ${maxpatternsize} \
                        -t ${threshold} \
                        -r ${run} \
                        -o ${outputfolder}/${outputName}/${dataset}_k${k}_run${run}.patterns \
                        ${outputfolder}/${dataset} \
                        > /dev/null \
                        2> ${outputfolder}/${outputName}/${dataset}_k${k}_run${run}.logs
                fi
            done
        done
    done
done
sem --id blub --wait
echo Done with processing
