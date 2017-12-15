#!/bin/bash

# Read dataset
dataset=$1
start_fold=$2
end_fold=$3
seed=$4

echo "Processing $dataset"

for (( i = $start_fold; i < $end_fold; i++ )); do
  for j in 0.1 0.2 0.3 0.4 0.5 0.7 0.9;do

    echo "Tunning with mutation $j"
    training=$dataset'-Training'$i'.csv'
    test=$dataset'-Test'$i'.csv'
    echo "Processing Fold $i"
    export OPENBLAS_NUM_THREADS=1
    python exec.py -dTr datasets/$dataset/$training -dTe datasets/$dataset/$test -ps 100 -gc 100 -mr $j -cr 0.7 -t 300 -s $seed -ti 1 -gr bnf/grammar_$dataset.bnf
  done
done
