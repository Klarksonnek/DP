# List of files created by Peter Tisovčík

```bash
├── dm
│   ├── AttributeUtil.py
│   ├── attrs
│   │   ├── AbstractPrepareAttr.py
│   │   ├── CO2VentilationLength.py
│   │   ├── FirstDifferenceAttrA.py
│   │   ├── GrowthRate.py
│   │   ├── __init__.py
│   │   ├── Regression.py
│   │   └── SecondDifferenceAttr.py
│   ├── coefficients
│   │   └── __init__.py
│   ├── ConnectionUtil.py
│   ├── co2regression
│   │   ├── AbstractRegression.py
│   │   ├── ExpRegressionWithDelay.py
│   │   ├── __init__.py
│   │   └── SimpleExpRegression.py
│   ├── DBUtil.py
│   ├── ExampleRunner.py
│   ├── Graph.py
│   ├── GraphUtil.py
│   ├── HeatMap.py
│   ├── __init__.py
│   ├── PreProcessing.py
│   ├── selectors
│   │   ├── __init__.py
│   │   ├── interval
│   │   │   └── __init__.py
│   │   └── row
│   │       ├── AbstractRowSelector.py
│   │       ├── __init__.py
│   │       ├── LinearSimpleCachedRowSelector.py
│   │       ├── SimpleCachedRowSelector.py
│   │       └── SimpleRowSelector.py
│   ├── SQLUtil.py
│   └── Storage.py
├── examples
│   └── events_peto.json
├── examples2
│   ├── 0000_db_tests
│   │   └── run.py
│   ├── 0200_open_close_all_graphs
│   │   └── run.py
│   ├── 0201_co2_delays_histogram
│   │   └── run.py
│   ├── 0202_open_detector
│   │   ├── co2
│   │   │   ├── gt_david.res
│   │   │   ├── gt_klarka.res
│   │   │   ├── gt_martin.res
│   │   │   ├── gt_peto.res
│   │   │   ├── 00.res
│   │   │   ├── 00.tgn
│   │   │   ├── 01.res
│   │   │   └── 01.tgn
│   │   ├── co2_t_h
│   │   │   ├── gt_david.res
│   │   │   ├── gt_klarka.res
│   │   │   ├── gt_martin.res
│   │   │   ├── gt_peto.res
│   │   │   ├── 00.res
│   │   │   ├── 00.tgn
│   │   │   ├── 01.res
│   │   │   └── 01.tgn
│   │   ├── co2_t_h_out
│   │   │   ├── gt_david.res
│   │   │   ├── gt_klarka.res
│   │   │   ├── gt_martin.res
│   │   │   ├── gt_peto.res
│   │   │   ├── 00.res
│   │   │   ├── 00.tgn
│   │   │   ├── 01.res
│   │   │   └── 01.tgn
│   │   ├── feature_stats.py
│   │   ├── run_co2.py
│   │   ├── run_co2_t_h_out.py
│   │   ├── run_co2_t_h.py
│   │   ├── runner_co2.py
│   │   ├── runner_co2_t_h_out.py
│   │   ├── runner_co2_t_h.py
│   │   └── start_end_stats.sh
│   └── 0203_open_ventilation_length_predictor
│       ├── performance_1.py
│       ├── performance_2.py
│       ├── run.py
│       └── stats.py
└── rm_processes
    └── processes_peto
        ├── clean
        │   ├── clean
        │   │   ├── DecisionTree.rmp
        │   │   ├── DeepLearning.rmp
        │   │   ├── NaiveBayes.rmp
        │   │   ├── NeuralNet.rmp
        │   │   ├── RandomForest.rmp
        │   │   └── SVM.rmp
        │   ├── co2
        │   │   ├── DecisionTree.rmp
        │   │   ├── DeepLearning.rmp
        │   │   ├── NaiveBayes.rmp
        │   │   ├── NeuralNet.rmp
        │   │   ├── RandomForest.rmp
        │   │   └── SVM.rmp
        │   ├── co2_t_h
        │   │   ├── DecisionTree.rmp
        │   │   ├── DeepLearning.rmp
        │   │   ├── NaiveBayes.rmp
        │   │   ├── NeuralNet.rmp
        │   │   ├── RandomForest.rmp
        │   │   └── SVM.rmp
        │   ├── co2_t_h_out
        │   │   ├── DecisionTree.rmp
        │   │   ├── DeepLearning.rmp
        │   │   ├── NaiveBayes.rmp
        │   │   ├── NeuralNet.rmp
        │   │   ├── RandomForest.rmp
        │   │   └── SVM.rmp
        │   ├── filter
        │   │   ├── correlation
        │   │   │   ├── DecisionTree.rmp
        │   │   │   ├── DeepLearning.rmp
        │   │   │   ├── NaiveBayes.rmp
        │   │   │   ├── NeuralNet.rmp
        │   │   │   ├── RandomForest.rmp
        │   │   │   └── SVM.rmp
        │   │   ├── gain_ratio
        │   │   │   ├── DecisionTree.rmp
        │   │   │   ├── DeepLearning.rmp
        │   │   │   ├── NaiveBayes.rmp
        │   │   │   ├── NeuralNet.rmp
        │   │   │   ├── RandomForest.rmp
        │   │   │   └── SVM.rmp
        │   │   ├── pca
        │   │   │   ├── DecisionTree.rmp
        │   │   │   ├── DeepLearning.rmp
        │   │   │   ├── NaiveBayes.rmp
        │   │   │   ├── NeuralNet.rmp
        │   │   │   ├── RandomForest.rmp
        │   │   │   └── SVM.rmp
        │   │   ├── relief
        │   │   │   ├── DecisionTree.rmp
        │   │   │   ├── DeepLearning.rmp
        │   │   │   ├── NaiveBayes.rmp
        │   │   │   ├── NeuralNet.rmp
        │   │   │   ├── RandomForest.rmp
        │   │   │   └── SVM.rmp
        │   │   └── svm
        │   │       ├── DecisionTree.rmp
        │   │       ├── DeepLearning.rmp
        │   │       ├── NaiveBayes.rmp
        │   │       ├── NeuralNet.rmp
        │   │       ├── RandomForest.rmp
        │   │       └── SVM.rmp
        │   └── wrapper
        │       ├── backward
        │       │   ├── DecisionTree.rmp
        │       │   ├── DeepLearning.rmp
        │       │   ├── NaiveBayes.rmp
        │       │   ├── NeuralNet.rmp
        │       │   ├── RandomForest.rmp
        │       │   └── SVM.rmp
        │       └── forward
        │           ├── DecisionTree.rmp
        │           ├── DeepLearning.rmp
        │           ├── NaiveBayes.rmp
        │           ├── NeuralNet.rmp
        │           ├── RandomForest.rmp
        │           └── SVM.rmp
        ├── ventilation_length
        │   ├── DecisionTree.rmp
        │   ├── DeepLearning.rmp
        │   ├── NaiveBayes.rmp
        │   ├── NeuralNet.rmp
        │   ├── RandomForest.rmp
        │   └── SVM.rmp
        └── with_cross
            ├── clean
            │   ├── DecisionTree.rmp
            │   ├── DeepLearning.rmp
            │   ├── NaiveBayes.rmp
            │   ├── NeuralNet.rmp
            │   ├── RandomForest.rmp
            │   └── SVM.rmp
            ├── filter
            │   ├── correlation
            │   │   ├── DecisionTree.rmp
            │   │   ├── DeepLearning.rmp
            │   │   ├── NaiveBayes.rmp
            │   │   ├── NeuralNet.rmp
            │   │   ├── RandomForest.rmp
            │   │   └── SVM.rmp
            │   ├── gain_ratio
            │   │   ├── DecisionTree.rmp
            │   │   ├── DeepLearning.rmp
            │   │   ├── NaiveBayes.rmp
            │   │   ├── NeuralNet.rmp
            │   │   ├── RandomForest.rmp
            │   │   └── SVM.rmp
            │   ├── pca
            │   │   ├── DecisionTree.rmp
            │   │   ├── DeepLearning.rmp
            │   │   ├── NaiveBayes.rmp
            │   │   ├── NeuralNet.rmp
            │   │   ├── RandomForest.rmp
            │   │   └── SVM.rmp
            │   ├── relief
            │   │   ├── DecisionTree.rmp
            │   │   ├── DeepLearning.rmp
            │   │   ├── NaiveBayes.rmp
            │   │   ├── NeuralNet.rmp
            │   │   ├── RandomForest.rmp
            │   │   └── SVM.rmp
            │   └── svm
            │       ├── DecisionTree.rmp
            │       ├── DeepLearning.rmp
            │       ├── NaiveBayes.rmp
            │       ├── NeuralNet.rmp
            │       ├── RandomForest.rmp
            │       └── SVM.rmp
            └── wrapper
                ├── backward
                │   ├── OptimizeSelectionDecisionTree.rmp
                │   ├── OptimizeSelectionDeepLearning.rmp
                │   ├── OptimizeSelectionNaiveBayes.rmp
                │   ├── OptimizeSelectionNeuralNet.rmp
                │   └── OptimizeSelectionSVM.rmp
                └── forward
                    ├── OptimizeSelectionDecisionTree.rmp
                    ├── OptimizeSelectionDeepLearning.rmp
                    ├── OptimizeSelectionNaiveBayes.rmp
                    ├── OptimizeSelectionNeuralNet.rmp
                    └── OptimizeSelectionSVM.rmp

```