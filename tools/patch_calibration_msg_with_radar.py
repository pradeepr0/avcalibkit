#! /usr/bin/env python3
# flake8: noqa

import os
from os import read
import sys
from datetime import datetime

import google.protobuf.text_format as pbtxtfmt
from pb.lyft.avsoftware.calibration.calibration_pb2 import \
    VehicleCalibrationProto, CalibrationDataSegmentProto, CalibrationDataGroupProto


def read_calibration_pbmsg_file(filename):
    msg = VehicleCalibrationProto()
    if filename.endswith('.pb') or filename.endswith('.pbcal'):
        with open(filename, 'rb') as f:
            msg.ParseFromString(f.read())
    elif filename.endswith('.pbtxt'):
        with open(filename, 'r') as f:
            msg = pbtxtfmt.Merge(f.read(), msg)
    return msg


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Patch a calibration .pb{cal,txt} file with an radar extrinsics update")
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
    parser.add_argument('patch_msg', type=str,
        help=".pb{cal,txt} file containing a `VehicleCalibrationProto` message with the radar" +
             " extrinsics update. Other information in this file is ignored.")
    args = parser.parse_args()

    # If `args.src_msg` is a valid hostname then set it to an actual filename
    link_file = '/etc/avcalibration/{}/valid_calibration.txt'.format(args.src_msg)
    if os.path.isfile(link_file):
        with open(link_file, 'r') as f:
            actual_filename = f.read().rstrip('\n')
        args.src_msg =  os.path.join(os.path.dirname(link_file), actual_filename)

    vehicle_calib = read_calibration_pbmsg_file(args.src_msg)
    patch_calib = read_calibration_pbmsg_file(args.patch_msg)

    # Update `vehicle_calib` with data from patch
    del vehicle_calib.radars[:]
    vehicle_calib.radars.extend(patch_calib.radars)

    src_rdata_group = [ g for g in vehicle_calib.calibration_dataset.carturner_calibration_data.groups
                             if g.process == CalibrationDataGroupProto.CAMERA_RADAR_CALIBRATION ]
    if not src_rdata_group:
        src_rdata_group = [ vehicle_calib.calibration_dataset.carturner_calibration_data.groups.add() ]
    src_rdata_group = src_rdata_group[0]

    patch_rdata_group = [ g for g in patch_calib.calibration_dataset.carturner_calibration_data.groups
                          if g.process == CalibrationDataGroupProto.CAMERA_RADAR_CALIBRATION ][0]

    src_rdata_group.process = CalibrationDataGroupProto.CAMERA_RADAR_CALIBRATION
    del src_rdata_group.segments[:]
    src_rdata_group.segments.extend(patch_rdata_group.segments)

    if args.out_format == 'pbtxt':
        print(vehicle_calib)
    else:
        assert args.out_format == 'pb'
        sys.stdout.buffer.write(vehicle_calib.SerializeToString())

if __name__ == '__main__':
    main()
