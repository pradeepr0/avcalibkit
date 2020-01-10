#! python3

import os
import glob


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Generate symlinks for valid_calibration.txt files within a avcalibration repo")
    parser.add_argument('git_root', nargs='*',
        help="Root dir for the avcalibration repo. Defauts to `/etc/avcalibration`")
    args = parser.parse_args()

    if not args.git_root:
        args.git_root = "/etc/avcalibration"

    for valid_calib_txt in glob.iglob(args.git_root + '/**/valid_calibration.txt'):
        with open(valid_calib_txt) as f:
            actual_filename = f.read().rstrip('\n')
        dir = os.path.dirname(valid_calib_txt)
        src = os.path.join(dir, actual_filename)
        tgt = os.path.join(dir, "valid_calibration.pbcal")

        if os.path.islink(tgt):
            os.remove(tgt)
        os.symlink(src, tgt)

if __name__ == '__main__':
    main()
