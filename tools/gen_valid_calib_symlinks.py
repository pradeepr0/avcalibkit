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

    for valid_calib_txt in sorted(glob.iglob(args.git_root + '/**/valid_calibration.txt')):
        with open(valid_calib_txt) as f:
            actual_filename = f.read().rstrip('\n')
        dir = os.path.dirname(valid_calib_txt)
        tgt = os.path.join(dir, actual_filename)
        symlink = os.path.join(dir, "valid_calibration.pbcal")

        requires_update = False
        if os.path.islink(symlink):
            if os.readlink(symlink) == tgt:
                continue
            else:
                requires_update = True
                os.remove(symlink)

        os.symlink(tgt, symlink)
        if not args.quiet:
            print('Updated' if requires_update else 'Created', symlink)
            print('  -> ', tgt)


if __name__ == '__main__':
    main()
