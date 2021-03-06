#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

from downward.reports.compare import ComparativeReport

import common_setup
from common_setup import IssueConfig, IssueExperiment
from relativescatter import RelativeScatterPlotReport

DIR = os.path.dirname(os.path.abspath(__file__))
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REVISIONS = ["issue578-v1"]
CONFIGS = [
    IssueConfig('cpdbs-hc900', ['--search', 'astar(cpdbs(patterns=hillclimbing(max_time=900)))']),
    IssueConfig('cpdbs-hc900-dp30', ['--search', 'astar(cpdbs(patterns=hillclimbing(max_time=900),dominance_pruning_max_time=30))']),
    IssueConfig('cpdbs-hc900-dp60', ['--search', 'astar(cpdbs(patterns=hillclimbing(max_time=900),dominance_pruning_max_time=60))']),
    IssueConfig('cpdbs-hc900-dp300', ['--search', 'astar(cpdbs(patterns=hillclimbing(max_time=900),dominance_pruning_max_time=300))']),
    IssueConfig('cpdbs-sys2', ['--search', 'astar(cpdbs(patterns=systematic(2)))']),
    IssueConfig('cpdbs-sys2-dp30', ['--search', 'astar(cpdbs(patterns=systematic(2),dominance_pruning_max_time=30))']),
    IssueConfig('cpdbs-sys2-dp60', ['--search', 'astar(cpdbs(patterns=systematic(2),dominance_pruning_max_time=60))']),
    IssueConfig('cpdbs-sys2-dp300', ['--search', 'astar(cpdbs(patterns=systematic(2),dominance_pruning_max_time=300))']),
]
SUITE = common_setup.DEFAULT_OPTIMAL_SUITE
ENVIRONMENT = BaselSlurmEnvironment(email="silvan.sievers@unibas.ch")

if common_setup.is_test_run():
    SUITE = IssueExperiment.DEFAULT_TEST_SUITE
    ENVIRONMENT = LocalEnvironment(processes=1)

exp = IssueExperiment(
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_resource("custom_parser", "custom-parser.py")
exp.add_command("run-custom-parser", ["{custom_parser}"])
exp.add_suite(BENCHMARKS_DIR, SUITE)

attributes = exp.DEFAULT_TABLE_ATTRIBUTES
attributes.extend([
    "dominance_pruning_failed",
    "dominance_pruning_time",
    "dominance_pruning_pruned_subsets",
    "dominance_pruning_pruned_pdbs",
    "pdb_collection_construction_time",
])

exp.add_fetcher('data/issue578-v1-more-configs-eval')
exp.add_absolute_report_step(attributes=attributes)
#exp.add_comparison_table_step()

exp.run_steps()
