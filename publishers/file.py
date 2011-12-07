#!/usr/bin/python

import argparse
import os

# note we must insert this as position 0 since dispatch is a standard module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dispatch import run_dispatch, run_index_dispatch, register_filters

def main():
    parser = argparse.ArgumentParser(
            description='Publish a blog entry (or entries) to HTML')
    parser.add_argument('-g', '--guid', metavar='URI', default='http://localhost/',
            help='root guid in the form of a valid RFC 1808 URI')
    parser.add_argument('-i', '--index', action='store_true', default=False,
            help='write index.html file, possibly overriding it (note: if given with -f then the only one entry will be added to index)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--dir', metavar='DIR', dest='dirname',
            help='directory of entries to publish')
    group.add_argument('-f', '--file', metavar='FILE', dest='filename',
            help='filename of a single entry to publish')
    args = parser.parse_args()

    # collect input filenames
    if args.filename:
        files = [args.filename]
    else:
        try:
            files = [os.path.join(args.dirname, f) for f in os.listdir(args.dirname)
                    if os.path.splitext(os.path.join(args.dirname, f))[1] == '.txt']
        except OSError, e:
            parser.error(str(e))

    filter_dir = os.path.join(os.path.dirname(__file__), '..', 'filters')
    tmpl_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

    filters = register_filters(filter_dir)

    # publish each entry by dispatching it
    entries = []
    for f in files:
        out = os.path.splitext(f)[0] + '.html'
        print 'Publishing %s to %s' % (f, out)
        try:
            input_fp = open(f, 'r')
            output_fp = open(out, 'w')
        except IOError, e:
            parser.error(str(e))
        else:
            e = run_dispatch(input_fp, output_fp, args.guid, filters)
            entries.append(e)
            input_fp.close()
            output_fp.close()

    # publish index if requested
    if args.index:
        out = os.path.join(os.path.dirname(f), 'index.html')
        print 'Publishing index with %d entries to %s' % (len(entries), out)
        try:
            output_fp = open(out, 'w')
        except IOError, e:
            parser.error(str(e))
        else:
            run_index_dispatch(entries, output_fp, args.guid)
            output_fp.close()


if __name__ == '__main__':
    main()
