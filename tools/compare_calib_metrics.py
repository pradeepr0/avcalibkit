#! /usr/bin/env python3
# flake8: noqa
import os
import shutil
import datetime
from collections import defaultdict
from glob import glob

import numpy as np

from src.calibration.lib_calibration.metric_pb2 import MetricCollectionProto, MetricIdProto


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Summarize the difference in camera reprojection error between two metrics")
    parser.add_argument('pb_file_patterns', nargs=2, help="two patterns to compare")
    args = parser.parse_args()

    left_files = glob(args.pb_file_patterns[0])
    right_files = glob(args.pb_file_patterns[1])

    for file_pair in zip(left_files, right_files):
        metric_msgs = []
        for filename in file_pair:
            msg = MetricCollectionProto()
            with open(filename, 'rb') as f:
                msg.ParseFromString(f.read())
            metric_msgs.append(msg)

        left, right = metric_msgs
        grouped = defaultdict(list)
        from itertools import chain
        for metric in chain(left.metrics, right.metrics):
            if metric.id.description == "point-to-plane distance error, all frames all surfaces":
                #"reprojection error, all frames all surfaces":
                key = '{} ({})'.format(metric.id.description, ','.join(metric.id.sensors))
                grouped[key].append(metric)

        def stats(values):
            return np.array([ np.min(values), np.mean(values), np.max(values) ])

        def get_calibration_id():
            l_calib_id = file_pair[0].split('/')[-2].split('--')[0]
            r_calib_id = file_pair[1].split('/')[-2].split('--')[0]
            assert l_calib_id == r_calib_id
            return l_calib_id

        print(get_calibration_id(), end='')
        for descr, (l_metric, r_metric) in sorted(grouped.items()):
            l_stats = stats(np.abs(l_metric.values.values))
            r_stats = stats(np.abs(r_metric.values.values))
            unit = MetricIdProto.Unit.Name(l_metric.id.unit)
            print('\t{:+04.4f}\t{:+04.4f}\t{:+04.4f}'.format(*(r_stats - l_stats)), end='')
        print()

if __name__ == "__main__":
    main()
