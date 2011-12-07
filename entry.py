import os
from jinja2 import Environment, FileSystemLoader
import lxml.etree as ET

jenv = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

class Entry(object):
    required_meta = ['title', 'guid']
    date_format = '%d %b %Y'

    meta = []
    body = None
    published_date = None
    modified_date = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def guid_suffix(self):
        return self.meta.get('guid').rsplit('/', 1)[-1]

    def to_html_tree(self):
        tmpl = jenv.get_template('entry.html')
        t = tmpl.render(entry=self)
        return t
        #return ET.fromstring(t)
