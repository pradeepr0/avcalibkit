#! /usr/bin/env python3

import os


def main():
    with open(os.path.expanduser('~/.bash_history')) as f:
        bash_history = f.readlines()

    existing = set()
    deduped = []
    for line in bash_history:
        if line not in existing:
            deduped.append(line)
            existing.add(line)

    with open(os.path.expanduser('~/.bash_history'), 'w') as f:
        f.writelines(deduped)

if __name__ == "__main__":
    main()
