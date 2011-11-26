import lxml.etree as ET

from exc import *

class Converter(object):
    def __init__(self, meta, body):
        self.meta = meta #: dict of metadata
        self.body = body #: block body

    def parse_title(self):
        """Subclasses should override this method to parse self.meta and
        return an lxml.etree.ElementTree of the title. Often this will
        simply just be a wrapper around meta['title']. 
        Note that this implementation simply returns an empty (and invalid) tree."""
        return ET.ElementTree()

    def parse_body(self):
        """Subclasses should override this method to parse self.body and
        return an lxml.etree.ElementTree of the entry's body text (or None if
        no body is required).
        Note that this implementation simply returns no body."""
        return None

converter_register = {
    'converter': Converter,
    'type': '<invalid>',
    'required_meta': ['title', 'guid'],
}
