from genshi.template import TemplateLoader
import lxml.etree as ET

_template_loader = TemplateLoader('templates', variable_lookup='strict')

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

    def to_html(self):
        t = _template_loader.load('entry.html').generate(entry=self).render('xhtml')
        return ET.fromstring(t)
