import datetime
import os
import urlparse
from jinja2 import Environment, FileSystemLoader

jenv = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

class Entry(object):
    required_meta = ['title', 'tag', 'published-date']
    on_disk_date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, meta, body, body_unfiltered, base_url):
        self.meta = meta
        self.body = body
        self._body = body_unfiltered
        self.base_url = base_url

    def __repr__(self):
        return '<Entry \'%s\' @ %s>' % (self.meta.get('tag'), self.published_date)

    @property
    def published_date(self):
        return datetime.datetime.strptime(self.meta.get('published-date'), 
                self.on_disk_date_format)

    @property
    def tag_specific(self):
        return self.meta.get('tag').split(':')[-1]

    @property
    def tag_name(self):
        return self.tag_specific.split('/')[-1]

    @property
    def output_filename(self):
        return None if self.is_linkroll else self.tag_name + '.html'

    @property
    def this_url(self):
        return self.meta.get('link') if self.is_linkroll \
                else urlparse.urljoin(self.base_url, self.tag_specific)

    @property
    def is_linkroll(self):
        return True if 'link' in self.meta else False

    @property
    def css_type(self):
        css = 'entry'
        if self.is_linkroll:
            css += ' linkroll'
        return css

    @property
    def summary(self):
        if self.body:
            if self.is_linkroll:
                return (self.body, False)
            else:
                s = self.body[:self.body.find('\n\n')]
                more = True
                if len(s) == len(self.body):
                    more = False
                return (s, more)
        else:
            return (None, False)

    def to_html_tree(self):
        def _join_url(url):
            return urlparse.urljoin(self.base_url, url)
        tmpl = jenv.get_template('entry.html')
        return tmpl.render(entry=self, 
                          join_url=_join_url)

class IndexOfEntries(object):
    def __init__(self, entries, base_url):
        self.entries = sorted(entries, key=lambda e: e.published_date, reverse=True)
        self.base_url = base_url

    def to_html_tree(self):
        def _join_url(url):
            return urlparse.urljoin(self.base_url, url)
        tmpl = jenv.get_template('index.html')
        return tmpl.render(entries=self.entries,
                           join_url=_join_url)
