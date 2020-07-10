#! /usr/bin/env python3
# flake8: noqa

import os
import subprocess
import shutil
import glob
import tempfile


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Generate python protobuf bindings for an `avsoftware` git tree")
    parser.add_argument('avs_root', type=str,
        help='Root of the `avsofware` git tree; .proto definitions are take from here')
    parser.add_argument('--idl_root', type=str,
        default=os.path.expanduser('~/idl/protos'),
        help='Root of the `idl` git repo tree; lyft idl .proto definitions are take from here')
    parser.add_argument('-o', '--out-dir', type=str,
        default=os.path.expanduser('~/avs_pyprotos'),
        help='Root folder for generated python bindings; defaults to `~/avspyprotos`')
    parser.add_argument('--verbose', dest='verbose', action='store_true', default=False)
    args = parser.parse_args()

    try:
        stage_dir = tempfile.mkdtemp(prefix='avs_pyprotos__', dir=os.path.dirname(args.out_dir))
        proto_files = glob.glob(args.avs_root + "/src/**/*.proto", recursive=True)
        proto_files += glob.glob(args.idl_root + "/pb/lyft/avsoftware/**/*.proto", recursive=True)
        print('Generating protobuf python bindings ...\n')
        for proto_file in proto_files:
            if args.verbose: print('  ' + proto_file)
            subprocess.call(['protoc', '-I', args.avs_root, '-I', args.idl_root,
                             '--python_out', stage_dir, proto_file])
        shutil.rmtree(args.out_dir, ignore_errors=True)
        os.rename(stage_dir, args.out_dir)
    except:
        if os.path.exists(stage_dir):
            shutil.rmtree(stage_dir)
        raise

    print('\nCreating python packages ...\n')
    for dir, _files, _subdirs in os.walk(args.out_dir):
        filename = os.path.join(dir, '__init__.py')
        with open(filename, 'w') as f:
            pass
        if args.verbose: print('  ' + filename)

if __name__ == "__main__":
    main()
