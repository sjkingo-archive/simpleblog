import email
import importlib
import os

import lxml.etree as ET

from exc import *

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

def register_converters(converter_dir='converters'):
    mods = set()
    dirs = [f for f in os.listdir(converter_dir) 
            if os.path.isdir(os.path.join(converter_dir, f))]
    for d in dirs:
        mod_name = '%s.%s' % (converter_dir, d)
        try:
            m = importlib.import_module(mod_name)
        except ImportError, e:
            raise InvalidConverter(str(e))
        if not hasattr(m, 'converter_register'):
            raise InvalidConverter('converter_register not defined for %s' % mod_name)
        for i in ['converter', 'type', 'required_meta']:
            if i not in m.converter_register:
                raise InvalidConverter('converter_register does not define `%s` for %s' 
                        % (i, mod_name))
        mods.add(m)
        print 'Registered converter %s for type %s' % (d, m.converter_register['type'])
    return mods

def run_dispatch(input_fp, output_fp, converters, filters=[]):
    # parse like a MIME document
    msg = email.message_from_file(input_fp)
    meta = dict(msg.items())
    body = msg.get_payload()

    # pick the correct dispatcher
    dispatcher = None
    for mod in converters:
        if meta.get('entry-type') == mod.converter_register.get('type'):
            dispatcher = mod
    if dispatcher is None:
        raise UnknownEntryType(meta.get('entry-type'))

    # validate the meta given
    for r in dispatcher.converter_register.get('required_meta'):
        if r not in meta:
            raise InvalidEntry('%s not present in entry meta' % r)

    # pass the body through any registered filters
    for filter_mod in filters:
        body = filter_mod.filter_register.get('callback')(body)

    entry = dispatcher.converter_register.get('converter')(meta, body)
    title_tree = entry.parse_title()
    assert type(title_tree) == ET._ElementTree, \
            'parse_title() did not return an ElementTree'
    output_fp.write(ET.tostring(title_tree, pretty_print=True))

    body_tree = entry.parse_body()
    assert body_tree is None or type(body_tree) == ET._ElementTree, \
            'parse_body() did not return an ElementTree or None'
    if body_tree is not None:
        output_fp.write(ET.tostring(body_tree, pretty_print=True))
