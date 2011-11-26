#!/usr/bin/python

import argparse
import os

from dispatch import run_dispatch, register_filters, register_converters

def main():
    parser = argparse.ArgumentParser(
            description='Publish a blog entry (or entries) to HTML')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--dir', metavar='DIR', dest='dirname',
            help='directory of entries to publish')
    group.add_argument('-f', '--file', metavar='FILE', dest='filename',
            help='filename of a single entry to publish')
    args = parser.parse_args()

    cons = register_converters()
    filters = register_filters()

    if args.filename:
        files = [args.filename]
    else:
        files = [os.path.join(args.dirname, f) for f in os.listdir(args.dirname)
                if os.path.splitext(os.path.join(args.dirname, f))[1] == '.txt']

    for f in files:
        with open(f, 'r') as fp:
            run_dispatch(fp, cons, filters)


if __name__ == '__main__':
    main()
