#!/bin/bash

# -split-percentage <percentage>
#	Sets the percentage for the train/test set split, e.g., 66.
#
# -x <number of folds>
#	Sets number of folds for cross-validation (default: 10).
#
# -T <name of test file>
#	Sets test file. If missing, a cross-validation will be performed
#	on the training data.


WEKA="/home/panda/gits/diplomka/Peto/test.arff"

cd /home/panda/Stažené/weka-3-8-2

java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.trees.J48 \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -C 0.25 -M 2

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.rules.ZeroR \
     -t "/home/panda/gits/diplomka/Peto/test.arff"

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.bayes.BayesNet \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E \
     weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 

#########################
# zaciatok pre split
#########################
SPLIT=66

echo "+++++++++ split-percentage ${SPLIT} ++++++++++++"

java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -split-percentage ${SPLIT} \
     -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a 

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.trees.J48 \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -split-percentage ${SPLIT} \
     -C 0.25 -M 2 

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.rules.ZeroR \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -split-percentage ${SPLIT}

echo "++++++++++++++++++++++++++++++++++++++++++++++++"

java -cp weka.jar weka.classifiers.bayes.BayesNet \
     -t "/home/panda/gits/diplomka/Peto/test.arff" \
     -split-percentage ${SPLIT} \
     -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E \
     weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5 

