#! /usr/bin/env python3
# flake8: noqa

import os
import sys
from datetime import datetime

import google.protobuf.text_format as pbtxtfmt
from src.calibration.lib_calibration.calibration_pb2 import \
    VehicleCalibrationProto, CalibrationDataSegmentProto, CalibrationDataGroupProto


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Patch a calibration .pb{cal,txt} file with an update")
    parser.add_argument('-f', '--out-format', choices=['pbtxt', 'pb'],
        default='pbtxt',
        help='Output format: protobuf binary or text.')
    parser.add_argument('-q', '--quiet', action='store_true',
        default=False,
        help='Do not print patch information')
    parser.add_argument('src_msg', type=str,
        help='`valid_calibration.pbcal` or `valid_calibration.pbtxt` or host-name. '
        'If hostname (e.g. `host-a007`) is specified then use the latest valid '
        'calibration for that host from `/etc/avcalibration/`')
    parser.add_argument('data_segment_msg', type=str,
        help='time_cam_lidar.pbtxt` file containing a `CalibrationDataSegmentProto` message')
    args = parser.parse_args()


    # If `args.src_msg` is a valid hostname then set it to an actual filename
    link_file = '/etc/avcalibration/{}/valid_calibration.txt'.format(args.src_msg)
    if os.path.isfile(link_file):
        with open(link_file, 'r') as f:
            actual_filename = f.read().rstrip('\n')
        args.src_msg =  os.path.join(os.path.dirname(link_file), actual_filename)

    vehicle_calib = VehicleCalibrationProto()
    if args.src_msg.endswith('.pb') or args.src_msg.endswith('.pbcal'):
        with open(args.src_msg, 'rb') as f:
            vehicle_calib.ParseFromString(f.read())
    elif args.src_msg.endswith('.pbtxt'):
        with open(args.src_msg, 'r') as f:
            vehicle_calib = pbtxtfmt.Merge(f.read(), vehicle_calib)

    with open(args.data_segment_msg, 'r') as f:
        data_segment = CalibrationDataSegmentProto()
        pbtxtfmt.Merge(f.read(), data_segment)

    # Update `vehicle_calib` with data from patch
    for group in vehicle_calib.calibration_dataset.carturner_calibration_data.groups:
        for segment in group.segments:
            if segment.process_type == data_segment.process_type:
                assert data_segment.process_type == CalibrationDataGroupProto.CAMERA_LIDAR_CALIBRATION
                segment.CopyFrom(data_segment)

    if args.out_format == 'pbtxt':
        print(vehicle_calib)
    else:
        assert args.out_format == 'pb'
        sys.stdout.buffer.write(vehicle_calib.SerializeToString())

    if not args.quiet:
        print('# Patch start time:\n#  ',
            datetime.fromtimestamp(data_segment.start_timestamp_unix_ns / 1e9).ctime(),
            file=sys.stderr)
        print('# Patch stop time:\n#  ',
            datetime.fromtimestamp(data_segment.stop_timestamp_unix_ns / 1e9).ctime(),
            file=sys.stderr)

if __name__ == '__main__':
    main()
