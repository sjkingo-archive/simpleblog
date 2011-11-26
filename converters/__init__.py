import lxml.etree as ET

from exc import *

globally_required_meta = ['entry-type', 'title', 'guid']

class Converter(object):
    #: metadata required by this converter
    locally_required_meta = []

    def __init__(self, meta, body):
        self.meta = meta #: dict of metadata
        self.body = body #: block body, to be parsed by markdown
        for r in self.locally_required_meta:
            if r not in meta:
                raise InvalidEntry('%s not present in entry' % r)

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
