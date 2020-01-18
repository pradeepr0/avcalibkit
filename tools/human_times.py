#! /usr/bin/env python3
"""
human_times.py

Looks for lines matching the pattern:
    `'.*timestamp.*:\s+(?P<TSVALUE>\d+)'`
in the input file(s) and annotates the input with a human understandable
conversions for each `TSVALUE`.
"""

import fileinput
from datetime import datetime


def main():
    for line in fileinput.input():
        if 'timestamp' in line:
            ts = int(line.strip().split()[-1])
            human_time = datetime.fromtimestamp(ts / 1e9).ctime()
            print('{}\t# {}'.format(line.rstrip('\n'), human_time))
        else:
            print(line, end='')

if __name__ == '__main__':
    main()
