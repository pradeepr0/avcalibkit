#! /usr/bin/env python3

import os
import glob




def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Generate symlinks for valid_calibration.txt files within a avcalibration repo")
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
        help="Do not print created / updated symlinks")
    parser.add_argument('git_root', nargs='*',
        help="Root dir for the avcalibration repo. Defauts to `/etc/avcalibration`")
    args = parser.parse_args()

    if not args.git_root:
        args.git_root = "/etc/avcalibration"

    ARTIFACTORY_BASE_URL = "https://artifactory.pdx.aws.av.lyft.net/repository/av-calibration"

    for valid_calib_txt in sorted(glob.iglob(args.git_root + '/**/valid_calibration.txt')):
        with open(valid_calib_txt) as f:
            actual_filename = f.read().rstrip('\n')
        dir = os.path.dirname(valid_calib_txt)
        relative_url = dir[len(args.git_root):]
        print("curl -T "
              "'{dir}/{actual_filename}' "
              "'{ARTIFACTORY_BASE_URL}/{relative_url}/{actual_filename}'".format(**locals()))

    for config_pb in sorted(glob.iglob(args.git_root + '/config/**/*.pb')):
        relative_url = config_pb[len(args.git_root):]
        print("curl -T "
              "'{config_pb}' "
              "'{ARTIFACTORY_BASE_URL}/{relative_url}'".format(**locals()))

if __name__ == '__main__':
    main()
