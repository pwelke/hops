#!/bin/env bash

exp='./util'


repetitions=`seq 1 10`
embOps='hops ps bps' 
outputFolders='chemical random social threshold'

# functions for plotting

function embOpColor {
    case $1 in
        hops) echo hopscolor ;;
        bps) echo bpscolor ;;
        ps) echo pscolor ;;
        *) echo black ;;
    esac
}

function embOpMark {
    case $1 in
        hops) echo \\hoPSmark ;;
        bps) echo \\BPSmark ;;
        ps) echo \\PSmark ;;
        *) echo . ;;
    esac
}


# functions for data collection

function getks {
    outputfolder=$1
    outputName=$2
    dataset=$3
    # find all output files
    # | remove their common prefix (important, dataset names may be strange)
    # | filter out the k parameter
    # | return the sorted, unique ks
    ls -1 ${outputfolder}/${outputName}/${dataset}_k* \
      | sed "s/${outputfolder}\/${outputName}\/${dataset}_k*//" \
      | cut --delimiter='_' --field=-1 \
      | sort --numeric-sort \
      | uniq
}

function getPatterns {
    outputfolder=$1
    outputName=$2
    dataset=$3
    k=$4

    ls ${outputfolder}/${outputName}/${dataset}_k${k}_run*.patterns \
      | xargs wc -l \
      | head -n-1 \
      | sed -e 's/^[[:space:]]*//' \
      | cut --delimiter=' ' --fields=1 \
      | ${exp}/avg.py
}

function getTime {
    outputfolder=$1
    outputName=$2
    dataset=$3
    k=$4

    cat ${outputfolder}/${outputName}/${dataset}_k${k}_run*.time \
      | cut --delimiter=' ' --fields=3 \
      | ${exp}/avg.py
}


# actual plotting

for outputfolder in ${outputFolders}; do

    # find all datasets in the current folder
    datasets=`ls ${outputfolder}/*.txt | xargs basename --multiple`
    
    echo processing ${outputfolder}
    time (
    echo \\documentclass\{standalone\}
    echo
    
    echo \\usepackage\{xcolor\}
    echo \\definecolor\{pscolor\}\{RGB\}\{128,205,193\}
    echo \\definecolor\{bpscolor\}\{RGB\}\{223,194,125\}
    echo \\definecolor\{adcolor\}\{RGB\}\{128,205,193\}
    echo \\definecolor\{hopscolor\}\{RGB\}\{166,97,26\}
    echo \\definecolor\{obdcolor\}\{RGB\}\{223,194,125\}
    echo \\definecolor\{randomcolor\}\{RGB\}\{1,133,113\}
    echo
    
    echo \\newcommand\{\\hoPSmark\}\{triangle*\}
    echo \\newcommand\{\\PSmark\}\{otimes*\}
    echo \\newcommand\{\\BPSmark\}\{square*\}
    echo
    
    echo \\usepackage\{tikz\}
    echo \\usepackage\{pgfplots\}
    echo \\usepackage\{pgfplotstable\}
    echo \\pgfplotsset\{compat=1.8\}
    echo \\usetikzlibrary\{fit, calc, shapes, positioning, patterns, pgfplots.groupplots\}
    echo
    
    echo % `pwd`/${outputfolder}
    echo
    
    echo \\begin\{document\}
    echo

    for dataset in ${datasets}; do

        echo \\begin\{tikzpicture\}
        echo \\pgfplotsset\{every axis legend/.append style=\{at=\{\(1,0\)\},anchor=south east\}\}
        echo \\pgfkeys{/pgfplots/MyAxisStyle/.style=\{height=4cm,width=0.4\\linewidth,scale only axis, point meta=explicit symbolic\}\}
        echo \\begin\{axis\}[MyAxisStyle, name=RecallPlot, title=\{ `echo ${dataset} | sed 's/\_/\\\_/g'` \}, xlabel=\{Time [s]\}, ylabel=\{Number of Patterns\}, anchor=north west, xshift=1cm, legend pos=outer north east]
        echo

        for outputName in ${embOps}; do 
                    
            # find the ks that have existing runs 
            ks=`getks ${outputfolder} ${outputName} ${dataset}`
    
            echo % ${outputName} results
            echo \\addlegendentry\{ ${outputName} \}
            echo \\addplot[-, mark=`embOpMark ${outputName}`, mark size=0.7pt, color=`embOpColor ${outputName}`] plot coordinates \{
            for k in ${ks}; do 
                patterns=`getPatterns ${outputfolder} ${outputName} ${dataset} ${k}`
                time=`getTime ${outputfolder} ${outputName} ${dataset} ${k}`
                echo \( ${time}, ${patterns} \) [${k}]
            done
            echo \}\;
            echo
        done

        echo \\legend\{\}
        echo \\end\{axis\}
        echo \\end\{tikzpicture\}
        echo 
    done

    echo \\end\{document\}
    ) > ${outputfolder}/figs_budgetRuntime.tex
done
