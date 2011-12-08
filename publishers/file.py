#!/usr/bin/python

import argparse
import codecs
import os

# note we must insert this as position 0 since dispatch is a standard module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dispatch import run_dispatch, run_index_dispatch, run_atom_dispatch, register_filters

def main():
    parser = argparse.ArgumentParser(
            description='Publish a blog entry (or entries) to HTML')
    parser.add_argument('-b', '--base', metavar='URL', default='http://localhost/',
            help='base URL prepended to all generated references (ensure it has a trailing slash)')
    parser.add_argument('-i', '--index', action='store_true', default=False,
            help='write index page and atom feed, possibly overriding them (note: if given with -f then the only one entry will be added to each!)')
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
    filters = register_filters(filter_dir)

    # publish each entry by dispatching it
    entries = []
    for f in files:
        try:
            input_fp = codecs.open(f, 'r')
        except IOError, e:
            parser.error(str(e))
        else:
            e, html = run_dispatch(input_fp, args.base, filters)
            if e.output_filename is not None:
                out = os.path.join(os.path.dirname(f), e.output_filename)
                print 'Publishing %s to %s' % (f, out)
                with open(out, 'w') as output_fp:
                    output_fp.write(html)
            else:
                print 'Skipping publishing %s as it has no output' % f
            entries.append(e)
            input_fp.close()

    # publish index and atom feed if requested
    if args.index:
        out = os.path.join(os.path.dirname(f), 'index.html')
        print 'Publishing index with %d entries to %s' % (len(entries), out)
        i, html = run_index_dispatch(entries, args.base, filters)
        with open(out, 'w') as fp:
            fp.write(html)

        atom = os.path.join(os.path.dirname(f), 'feed.atom')
        print 'Publishing atom feed to %s' % atom
        a = run_atom_dispatch(entries, args.base)
        with codecs.open(atom, 'w', 'utf-8') as fp:
            fp.write(a.to_xml_tree())


if __name__ == '__main__':
    main()
