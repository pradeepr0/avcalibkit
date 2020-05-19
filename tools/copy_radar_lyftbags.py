#! /usr/bin/env python3
import os
import shutil
import datetime


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Copy radar calibration lyftbags to local disk using a schematic name")
    parser.add_argument('-d', '--data-dir', type=str, default=os.path.expanduser('~/data'),
        help="Directory to copy the lyftbags to")
    parser.add_argument('-c', '--car-id', type=str, default=None,
        help="Vehicle/host that was used to collect data")
    parser.add_argument('-n', '--dry-run', action='store_true',
        help="Do not actually copy files. Just print commands that would be executed")
    args = parser.parse_args()

    if not args.car_id:
        with open('/media/lyft/DATA/temp/calibration/HOSTNAME') as f:
            args.car_id = f.read().strip()
    if args.car_id.startswith("host-"):
        args.car_id = args.car_id[5:]
    print('Copying radar logs for vehicle {}'.format(repr(args.car_id)), flush=True)

    def src_filename(i):
        return '/media/lyft/DATA/temp/calibration/merged_cam_radar-{}.lyftbag'.format(i)

    for i in range(4):
        filename = src_filename(i)
        assert os.path.isfile(filename), "Missing required lyftbag: {}".format(filename)

    for radar_id in range(4):
        mtime = datetime.datetime.fromtimestamp(os.stat(src_filename(radar_id)).st_mtime)
        mtime_short = mtime.strftime('%m%d_%H%M')
        dest_filename = os.path.join(args.data_dir,
                                     '{}_asytx-{}_{}.lyftbag'.format(args.car_id, radar_id, mtime_short))
        print(src_filename(radar_id), '->', dest_filename)
        if not args.dry_run:
            shutil.copy2(src_filename(radar_id), dest_filename)

if __name__ == "__main__":
    main()
