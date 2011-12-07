import email
import importlib
import os
import sys
import urlparse

from exc import *
import entry

def register_filters(filter_dir='filters'):
    filter_dir = os.path.abspath(filter_dir)
    sys.path.insert(0, filter_dir)

    mods = set()

    dirs = [f for f in os.listdir(filter_dir) 
            if os.path.isdir(os.path.join(filter_dir, f))]

    for mod_name in dirs:
        try:
            m = importlib.import_module(mod_name)
        except ImportError, e:
            raise InvalidFilter(str(e))
        if not hasattr(m, 'filter_register'):
            raise InvalidFilter('filter_register not defined for %s' % mod_name)
        if 'callback' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `callback` for %s' % mod_name)
        mods.add(m)
        print 'Registered filter %s' % mod_name

    return mods

def run_dispatch(input_fp, output_fp, root_guid, filters=[]):
    # parse like a MIME document
    msg = email.message_from_file(input_fp)
    meta = dict(msg.items())
    body = msg.get_payload()

    # validate the meta given
    for r in entry.Entry.required_meta:
        if r not in meta:
            raise InvalidEntry('%s not present in entry meta' % r)

    # parse the root guid and extract the required elements
    up = urlparse.urlparse(root_guid)

    # pass the body through any registered filters
    for filter_mod in filters:
        body = filter_mod.filter_register.get('callback')(body)

    e = entry.Entry(meta=meta,
                    body=body,
                    guid_domain=up.netloc,
                    guid_base=up.path)
    output_fp.write(e.to_html_tree())
