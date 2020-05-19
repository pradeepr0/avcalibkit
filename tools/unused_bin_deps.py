#! /usr/bin/env python3

from functools import lru_cache
from pathlib import Path
import subprocess
from typing import List, Tuple, Set, Sequence, Dict


def cmd_output(cmd: List[str], valid_return_codes: Sequence[int]=set([0])) -> str:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert proc.returncode in valid_return_codes, \
           "command '{}' returned {}".format(' '.join(cmd), proc.returncode)
    return proc.stdout.decode()


def get_loader_path_resolutions(bin_path: str) -> Dict[str, str]:
    solib_paths = dict()
    for line in cmd_output(["ldd", "-d", "-r", str(bin_path)]).splitlines():
        line = line.strip()
        if ' => ' not in line:
            continue
        if line.startswith('linux-vdso.so.1') or \
            line.startswith('/lib64/ld-linux-x86-64.so.2'):
            continue
        libname, _, resolved_path, _ = line.split()
        solib_paths[libname] = resolved_path
    return solib_paths


def get_solibs(bin_path: str) -> Set[str]:
    return set(get_loader_path_resolutions(bin_path).keys())


@lru_cache(maxsize=None, typed=True)
def get_unused_solibs(bin_path: str) -> Set[str]:
    output = cmd_output(["ldd", "-d", "-r", "-u", str(bin_path)], {0, 1})
    return set(x.strip() for x in output.splitlines()[1:])


@lru_cache(maxsize=None, typed=True)
def get_used_solibs(bin_path: str) -> Set[str]:
    return get_solibs(bin_path) - get_unused_solibs(bin_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "Find the direct and indirect unused binary dependencies of a binary executable")
    parser.add_argument('bin_path', nargs=1,
        help="Binary file to analyze")
    args = parser.parse_args()

    all_libs = set(get_loader_path_resolutions(args.bin_path[0]).values())
    unused_libs = get_unused_solibs(args.bin_path[0])
    used_libs = all_libs - unused_libs
    print('\n'.join(unused_libs))

    def sum_file_sizes(filepaths: Sequence[str]) -> int:
        return sum(Path(p).stat().st_size for p in filepaths)

    def human_size(num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%5.1f %s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%3.1f %s%s" % (num, 'Yi', suffix)

    used_size, unused_size = sum_file_sizes(used_libs), sum_file_sizes(unused_libs)
    print('{}\t{}\t{}\t{}\t{:.2f}%'.format(len(used_libs), len(unused_libs),
                                      human_size(used_size), human_size(unused_size),
                                      used_size * 100. / (used_size + unused_size)))


if __name__ == '__main__':
    main()



    # libname_to_path = get_loader_path_resolutions(args.bin_path[0])

    # def resolve_unresolved(libnames: Set[str]) -> Set[str]:
    #     """ Lookup libnames and resolve them to actual file paths. Names
    #     that cannot be resolved are returned as is. This takes care of
    #     absolute library path names. """
    #     return set(libname_to_path.get(name, name) for name in libnames)

    # @lru_cache(maxsize=None, typed=True)
    # def recursive_find_unused(binfile_path: str) -> Set[str]:
    #     if not binfile_path.startswith('/') and binfile_path not in libname_to_path:
    #         print('Problem resolving {}. skipping ...'.format(binfile_path))
    #         return {}
    #     used, unused = get_used_solibs(binfile_path), get_unused_solibs(binfile_path)
    #     used, unused = resolve_unresolved(used), resolve_unresolved(unused)
    #     for so in used:
    #         uu = resolve_unresolved(recursive_find_unused(so))
    #         unused.update(uu - used)
    #     return unused

    # used_libs = resolve_unresolved(get_used_solibs(args.bin_path[0]))
    # unused_libs = recursive_find_unused(args.bin_path[0])

