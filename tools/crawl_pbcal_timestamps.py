#! /usr/bin/env python3
# flake8: noqa

from datetime import datetime
import os
from pathlib import Path
import sys


from src.calibration.lib_calibration.calibration_pb2 import VehicleCalibrationProto, CalibrationDataGroupProto


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Crawl all lyftbag timestamps from an avcalibration repository")
    parser.add_argument('avcalib_git_root', type=str, nargs='?',
        help='Root folder of the avcalibration repository. Defaults to `/etc/avcalibration/`')
    args = parser.parse_args()

    if not args.avcalib_git_root:
        args.avcalib_git_root = ['/etc/avcalibration']

    for pbcal_filename in Path(args.avcalib_git_root[0]).glob('**/*.pbcal'):
        msg = VehicleCalibrationProto()
        with pbcal_filename.open('rb') as f:
            msg.ParseFromString(f.read())
        hostname = 'host-' + msg.vehicle_meta_data.id.lower()
        data = msg.calibration_dataset.carturner_calibration_data
        for group in data.groups:
            gprocess = CalibrationDataGroupProto.Type.Name(group.process)
            for seg in group.segments:
                sprocess = CalibrationDataGroupProto.Type.Name(seg.process_type)
                print('\t'.join([hostname,
                                 str(seg.min_timestamp_unix_ns),
                                 str(seg.max_timestamp_unix_ns),
                                 str(datetime.fromtimestamp(seg.min_timestamp_unix_ns / 1e9)),
                                 str(datetime.fromtimestamp(seg.max_timestamp_unix_ns / 1e9)),
                                 gprocess, sprocess, seg.description,
                                 pbcal_filename.name]))

if __name__ == '__main__':
    main()
