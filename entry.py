import datetime
import os
from jinja2 import Environment, FileSystemLoader

jenv = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

class Entry(object):
    required_meta = ['title', 'guid', 'published-date']
    on_disk_date_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%d %b %Y'

    meta = []
    body = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def published_date(self):
        return datetime.datetime.strptime(self.meta.get('published-date'), 
                self.on_disk_date_format)

    @property
    def guid_suffix(self):
        return self.meta.get('guid').rsplit('/', 1)[-1]

    @property
    def is_linkroll(self):
        # TODO need to check against base guid
        return True

    @property
    def css_type(self):
        # TODO need to check against base guid
        css = 'entry'
        if self.is_linkroll:
            css += ' linkroll'
        return css

    def to_html_tree(self):
        tmpl = jenv.get_template('entry.html')
        t = tmpl.render(entry=self)
        return t
