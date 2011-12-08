import email
import importlib
import os
import sys

from exc import *
import entry

def filter_end(html, filters):
    # pass the templated page through any registered filters defined for end
    for filter_mod in [f for f in filters if f.filter_register.get('when') == 'end']:
        html = filter_mod.filter_register.get('callback')(html)
    return html

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
        if 'when' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `when` for %s' % mod_name)
        if m.filter_register.get('when') not in ['start', 'end']:
            raise InvalidFilter('filter_register.when has an invalid value for %s' % mod_name)
        mods.add(m)
        print 'Registered filter %s to run at %s' % (mod_name, m.filter_register.get('when'))

    return mods

def run_dispatch(input_fp, base_url, filters=[]):
    # parse like a MIME document
    msg = email.message_from_file(input_fp)
    meta = dict(msg.items())
    body_unfiltered = msg.get_payload()

    # validate the meta given
    for r in entry.Entry.required_meta:
        if r not in meta:
            raise InvalidEntry('%s not present in entry meta' % r)

    body = body_unfiltered.strip()
    if len(body) == 0:
        body = None
    else:
        # pass the body through any registered filters defined for start
        for filter_mod in [f for f in filters if f.filter_register.get('when') == 'start']:
            body = filter_mod.filter_register.get('callback')(body)

    e = entry.Entry(meta, body, body_unfiltered, base_url)
    html = filter_end(e.to_html_tree(), filters)
    return (e, html)

def run_index_dispatch(entries, base_url, filters=[]):
    i = entry.IndexOfEntries(entries, base_url)
    html = filter_end(i.to_html_tree(), filters)
    return (i, html)

def run_atom_dispatch(entries, base_url):
    return entry.AtomFeed(entries, base_url)
