import email

import lxml.etree as ET

from converters import globally_required_meta
from converters.blog import BlogEntry
from exc import *

dispatch_types = {
    'blog': BlogEntry,
}

def run_dispatch(fp):
    # parse like a MIME document
    msg = email.message_from_file(fp)
    meta = dict(msg.items())
    body = msg.get_payload()

    # validate the metadata
    for r in globally_required_meta:
        if r not in meta:
            raise InvalidEntry('%s not present in entry' % r)

    try:
        entry = dispatch_types[meta.get('entry-type')](meta, body)
    except KeyError:
        raise UnknownEntryType(meta.get('entry-type'))
    else:
        title_tree = entry.parse_title()
        assert type(title_tree) == ET._ElementTree, \
                'parse_title() did not return an ElementTree'
        print ET.tostring(title_tree, pretty_print=True)

        body_tree = entry.parse_body()
        assert body_tree is None or type(body_tree) == ET._ElementTree, \
                'parse_body() did not return an ElementTree or None'
        if body_tree is not None:
            print ET.tostring(body_tree, pretty_print=True)


run_dispatch(open('example_entries/blog_entry.txt', 'r'))
