#!/bin/bash

# Read dataset
dataset=$1
start_fold=$2
end_fold=$3
seed=$4

echo "Processing $dataset"

for (( i = $start_fold; i < $end_fold; i++ )); do

    training=$dataset'-Training'$i'.csv'
    test=$dataset'-Test'$i'.csv'
    echo "Processing Fold $i"
    export OPENBLAS_NUM_THREADS=1
    # python exec.py -dTr datasets/$dataset/$training -dTe datasets/$dataset/$test -ps 100 -gc 15 -mr 0.1 -cr 0.9 -t 300 -s $seed -ti 1 -gr bnf/grammar_$dataset.bnf
    python exec.py -dTr datasets/$dataset/$training -dTe datasets/$dataset/$test -ps 100 -gc 10 -mr 0.3 -cr 0.7 -t 300 -ft 60 -s $seed -ti 1 -gr bnf/new_ml2.bnf
done
