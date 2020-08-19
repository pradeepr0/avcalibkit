#! /usr/bin/env python3

import os
import glob




def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Print upload commands for uploading latest valid_calibration files to " +
        "avcalibration artifactory")
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
        print("curl -T "
              "'{dir}/{actual_filename}' "
              "'{ARTIFACTORY_BASE_URL}/{dir}/{actual_filename}'".format(**locals()))

    for config_pb in sorted(glob.iglob(args.git_root + '/config/**/*.pb')):
        print("curl -T "
              "'{config_pb}' "
              "'{ARTIFACTORY_BASE_URL}/{config_pb}'".format(**locals()))

if __name__ == '__main__':
    main()
