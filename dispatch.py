import email
import importlib
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from exc import *
import entry

def get_filters_for(filters, apply_to):
    return [f for f in filters 
            if f.filter_register.get('apply_to') == apply_to]

def apply_filters_for(filters, apply_to, s):
    for filter_mod in get_filters_for(filters, apply_to):
        s = filter_mod.filter_register.get('callback')(s)
    return s

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
        if 'enabled' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `enabled` for %s' % mod_name)
        if 'callback' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `callback` for %s' % mod_name)
        if 'apply_to' not in m.filter_register:
            raise InvalidFilter('filter_register does not define `apply_to` for %s' % mod_name)
        if m.filter_register.get('apply_to') not in ['entry_body', 'html_file']:
            raise InvalidFilter('filter_register.apply_to has an invalid value for %s' % mod_name)

        if m.filter_register.get('enabled'):
            mods.add(m)
            print 'Registered filter %s that will apply to %s' % (mod_name,
                    m.filter_register.get('apply_to'))
        else:
            print 'Not registering disabled filter %s' % mod_name

    return mods

def run_dispatch(input_fp, base_url, filters=[], disqus_shortname=None):
    # parse like a MIME document
    msg = email.message_from_file(input_fp)
    meta = dict(msg.items())
    body_unfiltered = msg.get_payload()

    body = body_unfiltered.strip()
    if len(body) == 0:
        body = None
    else:
        body = apply_filters_for(filters, 'entry_body', body)

    e = entry.Entry(meta, body, body_unfiltered, base_url, disqus_shortname)
    html = apply_filters_for(filters, 'html_file', e.to_html_tree())
    return (e, html)

def run_index_dispatch(entries, base_url, filters=[], disqus_shortname=None):
    i = entry.IndexOfEntries(entries, base_url, disqus_shortname)
    html = apply_filters_for(filters, 'html_file', i.to_html_tree())
    return (i, html)

def run_atom_dispatch(entries, base_url):
    return entry.AtomFeed(entries, base_url, disqus_shortname=None)
