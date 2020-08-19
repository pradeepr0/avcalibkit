import sys
import pathlib

import numpy as np
import scipy.io


def main():
    for ply_filepath in (pathlib.Path(a) for a in sys.argv[1:]):
        print('Processing {}...'.format(ply_filepath))
        with ply_filepath.open('r') as f:
            ascii_format = False
            for line in f:
                line = line.rstrip()
                if line == "format ascii 1.0":
                    ascii_format = True
                if line == "end_header":
                    assert ascii_format, "Only ascii format PLY files are supported"
                    data = np.array([ [float(x) for x in data_lines.split()]
                                                for data_lines in f ])
            mat_filepath = ply_filepath.parent / (ply_filepath.stem + ".mat")
            scipy.io.savemat(str(mat_filepath), mdict={mat_filepath.stem: data})
            print('  saved: {}'.format(mat_filepath))

if __name__ == '__main__':
    main()