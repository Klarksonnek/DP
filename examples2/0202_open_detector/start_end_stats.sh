#!/usr/bin/env bash

##

echo "co2 - start"
rm -f testing.csv training.csv out.csv
cp co2/training_cached.csv training.csv
cp co2/m4_testing.csv testing.csv
python3 feature_stats.py

echo "co2 - end"
rm -f testing.csv training.csv out.csv
cp co2/training.csv training.csv
cp co2/m4_testing.csv testing.csv
python3 feature_stats.py

##
echo "co2_t_h - start"
rm -f testing.csv training.csv out.csv
cp co2_t_h/training_cached.csv training.csv
cp co2_t_h/m4_testing.csv testing.csv
python3 feature_stats.py

echo "co2_t_h - end"
rm -f testing.csv training.csv out.csv
cp co2_t_h/training.csv training.csv
cp co2_t_h/m4_testing.csv testing.csv
python3 feature_stats.py

##
echo "co2_t_h_out - start"
rm -f testing.csv training.csv out.csv
cp co2_t_h_out/training_cached.csv training.csv
cp co2_t_h_out/m4_testing.csv testing.csv
python3 feature_stats.py

echo "co2_t_h_out - end"
rm -f testing.csv training.csv out.csv
cp co2_t_h_out/training.csv training.csv
cp co2_t_h_out/m4_testing.csv testing.csv
python3 feature_stats.py
