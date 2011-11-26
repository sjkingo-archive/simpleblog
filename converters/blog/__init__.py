import lxml.etree as ET

import converters

class BlogEntry(converters.Converter):
    def parse_title(self):
        a = ET.Element('a')
        a.set('href', self.meta.get('guid'))
        a.set('title', self.meta.get('title'))
        h2 = ET.SubElement(a, 'h2')
        h2.text = self.meta.get('title')
        return ET.ElementTree(a)

    def parse_body(self):
        entry_name = self.meta.get('guid').rsplit('/', 1)[-1]
        root = ET.Element('div')
        root.set('id', entry_name)
        root.set('class', 'blog_entry')
