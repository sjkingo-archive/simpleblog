import datetime
import email
import importlib
import os

import lxml.etree as ET

from exc import *
import entry

def register_filters(filter_dir='filters'):
    mods = set()
    dirs = [f for f in os.listdir(filter_dir) 
            if os.path.isdir(os.path.join(filter_dir, f))]
    for d in dirs:
        mod_name = '%s.%s' % (filter_dir, d)
        try:
            m = importlib.import_module(mod_name)
        except ImportError, e:
            raise InvalidFilter(str(e))
        if not hasattr(m, 'filter_register'):
            raise InvalidFilter('filter_register not defined for %s' % mod_name)
        if 'callback' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `callback` for %s' % mod_name)
        mods.add(m)
        print 'Registered filter %s' % d
    return mods

def setup_xslt(filename):
    return ET.XSLT(ET.parse(filename))

def run_dispatch(input_fp, output_fp, xslt, filters=[]):
    # parse like a MIME document
    msg = email.message_from_file(input_fp)
    meta = dict(msg.items())
    body = msg.get_payload()

    # validate the meta given
    for r in entry.Entry.required_meta:
        if r not in meta:
            raise InvalidEntry('%s not present in entry meta' % r)

    # pass the body through any registered filters
    for filter_mod in filters:
        body = filter_mod.filter_register.get('callback')(body)

    # extract the publication and modified dates
    st = os.stat(input_fp.name)
    published_date = datetime.datetime.fromtimestamp(st.st_ctime)
    modified_date = datetime.datetime.fromtimestamp(st.st_mtime)
    if modified_date == published_date:
        modified_date = None

    e = entry.Entry(meta=meta,
                    body=body,
                    published_date=published_date,
                    modified_date=modified_date)
    transformed = xslt(e.to_html())
    output_fp.write(ET.tostring(transformed, pretty_print=True))
