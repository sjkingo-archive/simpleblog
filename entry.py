import datetime
import os
import urlparse
from jinja2 import Environment, FileSystemLoader

jenv = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

class Entry(object):
    required_meta = ['title', 'tag', 'published-date']
    on_disk_date_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%d %b %Y'

    def __init__(self, meta, body, base_url):
        self.meta = meta
        self.body = body
        self.base_url = base_url

    def __repr__(self):
        return '<Entry \'%s\' @ %s>' % (self.meta.get('tag'), self.published_date)

    @property
    def published_date(self):
        return datetime.datetime.strptime(self.meta.get('published-date'), 
                self.on_disk_date_format)

    @property
    def tag_name(self):
        return self.meta.get('tag').split(':')[-1].split('/')[-1]

    @property
    def output_filename(self):
        return None if self.is_linkroll else self.tag_name + '.html'

    @property
    def this_url(self):
        return self.meta.get('link') if self.is_linkroll else \
                urlparse.urljoin(self.base_url, self.output_filename)

    @property
    def is_linkroll(self):
        return True if 'link' in self.meta else False

    @property
    def css_type(self):
        css = 'entry'
        if self.is_linkroll:
            css += ' linkroll'
        return css

    def to_html_tree(self):
        tmpl = jenv.get_template('entry.html')
        t = tmpl.render(entry=self)
        return t

class IndexOfEntries(object):
    def __init__(self, entries, base_url):
        self.entries = sorted(entries, key=lambda e: e.published_date)
        self.base_url = base_url

    def to_html_tree(self):
        return jenv.get_template('index.html').render(entries=self.entries)
