#!/usr/bin/env bash
"""Script for simplification of iterative training process.
"""
from dm.ExampleRunner import ExampleRunner as er

__author__ = 'Peter Tisovčík'
__email__ = 'xtisov00@stud.fit.vutbr.cz'


if __name__ == '__main__':
    # er.detector(2 * 60, 3 * 60, 'run_co2_t_h_out.py', '//DIP/clean/clean/NaiveBayes', True)
    er.feature_stats('run_co2_t_h_out.py', True)
