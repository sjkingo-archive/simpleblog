import datetime
import os
import urlparse
from jinja2 import Environment, FileSystemLoader

jenv = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates')))

ATOM_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S+10:00'

class InvalidEntry(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Entry(object):
    required_meta = frozenset(['title', 'guid', 'published-date'])
    optional_meta = frozenset(['link', 'modified-date'])
    on_disk_date_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self, meta, body, body_unfiltered, base_url,
            disqus_shortname):
        self.validate_entry(self, meta)

        self.meta = meta
        self.body = body
        self._body = body_unfiltered
        self.base_url = base_url
        self.disqus_shortname = disqus_shortname

    def __repr__(self):
        return '<Entry \'%s\' @ %s>' % (self.meta.get('guid'), self.published_date)

    @staticmethod
    def assert_tag(cls, guid):
        parts = guid.split(':')
        assert len(parts) == 3
        assert parts[0] == 'tag'
        entity = parts[1].split(',', 1)
        assert len(entity) == 2
        return (entity[0], entity[1], parts[2])

    @staticmethod
    def validate_entry(cls, meta):
        fset_head = frozenset(meta.keys())

        # make sure all required headers are present
        diff = cls.required_meta - fset_head
        if len(diff) != 0:
            raise InvalidEntry('missing required header(s): %s' % list(diff))

        # make sure there are no additional headers
        diff = fset_head - cls.required_meta - cls.optional_meta
        if len(diff) != 0:
            raise InvalidEntry('entraneous header(s) found: %s' % list(diff))

        # validate the guid
        try:
            cls.assert_tag(cls, meta.get('guid'))
        except AssertionError:
            raise InvalidEntry('guid is an invalid tag according to RFC4151')

    @property
    def published_date(self):
        return datetime.datetime.strptime(self.meta.get('published-date'), 
                self.on_disk_date_format)

    @property
    def modified_date(self):
        m = self.meta.get('modified-date', None)
        if m is None:
            return None
        else:
            return datetime.datetime.strptime(m, self.on_disk_date_format)

    @property
    def guid_specific(self):
        return self.meta.get('guid').split(':')[-1]

    @property
    def guid_name(self):
        return self.guid_specific.split('/')[-1]

    @property
    def output_filename(self):
        return self.guid_name + '.html'

    @property
    def this_url(self):
        return self.meta.get('link') if self.is_link \
                else urlparse.urljoin(self.base_url, self.guid_specific)

    @property
    def permalink(self):
        return urlparse.urljoin(self.base_url, self.guid_specific)

    @property
    def is_link(self):
        return True if 'link' in self.meta else False

    @property
    def css_type(self):
        css = 'entry'
        if self.is_link:
            css += ' link'
        return css

    @property
    def summary(self):
        if self.body:
            if self.is_link:
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
    def __init__(self, entries, base_url, disqus_shortname):
        self.entries = sorted(entries, key=lambda e: e.published_date, reverse=True)
        self.base_url = base_url
        self.disqus_shortname = disqus_shortname

    def to_html_tree(self):
        def _join_url(url):
            return urlparse.urljoin(self.base_url, url)
        tmpl = jenv.get_template('index.html')
        return tmpl.render(entries=self.entries,
                           join_url=_join_url,
                           disqus_shortname=self.disqus_shortname)

class AtomFeed(IndexOfEntries):
    def to_xml_tree(self):
        def _join_url(url):
            return urlparse.urljoin(self.base_url, url)

        max_d = max(e.published_date for e in self.entries)

        tmpl = jenv.get_template('feed.atom')
        return tmpl.render(entries=self.entries,
                           join_url=_join_url,
                           latest_published_date=max_d,
                           ATOM_DATE_FORMAT=ATOM_DATE_FORMAT)
