#! /usr/bin/env python3

from pathlib import Path
import requests
import re


def main():
    import argparse
    parser = argparse.ArgumentParser(
        "List full and relative URLs of files on avcalibration artifactory. For each file found, "
        "the full URL and the relative URL path are printed out, separated by a TAB character.")
    parser.add_argument('base_urls', nargs='+',
        help="List of artifactory URLs")
    parser.add_argument('--curl', action='store_true',
        help="Print curl commands to download files instead of listing them. "
             "Pipe these commands to gnu-parallel to download files in parallel; "
             "For example, `crawl_files.py URL | parallel --bar -j 100`")
    parser.add_argument('--curl-out-dir', type=Path, default=Path('/media/data/temp/'),
        help="Modify curl command to save files to specified folder")
    args = parser.parse_args()

    if not args.base_urls:
        args.base_urls = ["/"]

    args.base_urls = [ u.rstrip('/') + '/' for u in args.base_urls ]

    def list_files_recursive(url):
        r = requests.get(url)
        r.raise_for_status()
        for m in re.finditer('href="(.*)"', r.text):
            entry = m.group(1)
            if entry == "../":
                continue
            elif entry.endswith("/"):
                yield from list_files_recursive(url + entry)
            else:
                file_url = url + entry
                yield file_url

    for base_url in args.base_urls:
        for file_url in list_files_recursive(base_url):
            protocol_, slash_, server, path = file_url.split('/', maxsplit=3)
            if not args.curl:
                print(file_url)
            else:
                print("curl -sS --create-dirs '{}' -o '{}'".format(file_url, args.curl_out_dir / path))


if __name__ == '__main__':
    main()
