#!/usr/bin/python

import argparse
import codecs
import os

# note we must insert this as position 0 since dispatch is a standard module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dispatch import run_dispatch, run_index_dispatch, run_atom_dispatch, register_filters
from entry import InvalidEntry

def main():
    parser = argparse.ArgumentParser(
            description='Publish a blog entry (or entries) to HTML')
    parser.add_argument('-d', '--dir', metavar='DIR', dest='dirname', required=True,
            help='directory of entries to publish')
    parser.add_argument('-b', '--base', metavar='URL', default='http://localhost/',
            help='base URL prepended to all generated references (ensure it has a trailing slash)')
    parser.add_argument('-D', '--disqus_shortname', metavar='SHORTNAME',
            help='shortname for disqus comments (if not given, comments are disabled')
    args = parser.parse_args()

    try:
        files = [os.path.join(args.dirname, f) for f in os.listdir(args.dirname)
                if os.path.splitext(os.path.join(args.dirname, f))[1] == '.txt']
    except OSError, e:
        parser.error(str(e))

    filter_dir = os.path.join(os.path.dirname(__file__), '..', 'filters')
    filters = register_filters(filter_dir)

    # publish each entry by dispatching it
    entries = []
    published = []
    for f in files:
        try:
            input_fp = codecs.open(f, 'r')
        except IOError, e:
            parser.error(str(e))
        else:
            try:
                et, html = run_dispatch(input_fp, args.base, filters, 
                        args.disqus_shortname)
            except InvalidEntry, e:
                print >> sys.stderr, 'Error in %s: %s' % (f, str(e))
                exit(3)
            if et.output_filename is not None:
                out = os.path.join(os.path.dirname(f), et.output_filename)
                publish = False
                try:
                    with codecs.open(out, 'r', 'utf-8') as output_fp:
                        h = output_fp.read()
                        if h != html:
                            publish = True
                except IOError:
                    publish = True
                if publish:
                    print 'Publishing %s to %s' % (f, out)
                    with codecs.open(out, 'w', 'utf-8') as output_fp:
                        output_fp.write(html)
                    published.append(et)
            entries.append(et)
            input_fp.close()

    print 'Published %d entries' % len(published)

    # publish index and atom feed
    if len(published) != 0:
        out = os.path.join(os.path.dirname(f), 'index.html')
        print 'Publishing index with %d entries to %s' % (len(entries), out)
        i, html = run_index_dispatch(entries, args.base, filters,
                args.disqus_shortname)
        with open(out, 'w') as fp:
            fp.write(html)

        atom = os.path.join(os.path.dirname(f), 'feed.atom')
        print 'Publishing atom feed to %s' % atom
        a = run_atom_dispatch(entries, args.base)
        with codecs.open(atom, 'w', 'utf-8') as fp:
            fp.write(a.to_xml_tree())


if __name__ == '__main__':
    main()
