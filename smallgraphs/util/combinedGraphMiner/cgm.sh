#!/usr/bin/env bash

# requirements
# gnu parallel
# gaston 
# lwg


function gaston {
	# local aids2gaston='../../smallgraphs/gfc'
	local aids2gaston='../converter/aids2gaston.py'
	local gaston2aids='../converter/gaston2aids.py'
	local gaston='../gaston-1.1/gaston'

	local max_psize=$1
	local min_support=$2
	local input_file=$3
	local output_patterns=$4
	local output_features=$5
	local ignored_sampling_pam=$6

	# temp output
	input_file_tmp=gaston_in_tmp
	output_patterns_tmp=gaston_out_tmp

	# debugging
	echo gaston parameters are max_psize=${max_psize} min_support=${min_support} input_file=${input_file} output_patterns=${output_patterns} output_features=${output_features}
	wc -l ${input_file}

	# convert from aids format
	${formatConverter} < ${input_file} > ${input_file_tmp}
	# frequent tree mining
	echo ${gaston} -m ${max_psize} -t ${min_support} ${input_file_tmp} # ${output_patterns_tmp}
	local gastonpid=$!
	
	echo gaston pid is ${gastonpid} 

	# convert output
	# ${gaston2aids} < ${output_patterns_tmp} > ${output_patterns}

	# remove tempfiles
	# rm ${input_file_tmp}
	# rm ${output_patterns_tmp}
}


function probabilistic_mining {
	local lwg='../bin/lwg'

	local max_psize=$1
	local min_support=$2
	local input_file=$3
	local output_patterns=$4
	local output_features=$5
	local sampling_param=$6

	# temp output
	input_file_tmp=lwg_in_tmp
	output_patterns_tmp=lwg_out_tmp
	output_features_tmp=lwg_out_feat_tmp

	# debugging
	echo prob mining parameters are max_psize=${max_psize} min_support=${min_support} input_file=${input_file} output_patterns=${output_patterns} output_features=${output_features}
	wc -l ${input_file}

	${lwg} -p ${max_psize} -t ${min_support} \
	  -e localEasySampling -i ${sampling_param} \
	  -o ${output_patterns_tmp} < ${input_file} > ${output_features_tmp} 
}


max_psize=10
sampling_param=5
min_support=20
input_file='MUTAG.txt'
output_patterns=MUTAG.output_patterns
output_features=MUTAG.output_features


export -f probabilistic_mining
export -f gaston

# parallel --jobs 2 --tag \
#   "{} ${max_psize} ${min_support} ${input_file} {}_${output_patterns} {}_${output_features}" \
#   ::: probabilistic_mining gaston
  
probabilistic_mining ${max_psize} ${min_support} ${input_file} probabilistic_mining_${output_patterns} probabilistic_mining_${output_features} ${sampling_param}

gaston               ${max_psize} ${min_support} ${input_file} gaston_${output_patterns} gaston_${output_features} ${sampling_param}
  

  # probabilistic_mining ${max_psize} ${min_support} ${input_file} ${output_patterns} ${output_features}

# sem --jobs 2 --tag \
#   gaston ${max_psize} ${min_support} ${input_file} ${output_patterns} ${output_features}