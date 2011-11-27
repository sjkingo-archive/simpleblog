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

        pub_date = ET.SubElement(root, 'div')
        pub_date.set('id', 'published-date')
        pub_date.set('title', self.published_date.isoformat())
        pub_date.text = self.published_date.strftime(self.date_format)

        if self.modified_date is not None:
            mod_date = ET.SubElement(root, 'div')
            mod_date.set('id', 'modified-date')
            mod_date.set('title', self.modified_date.isoformat())
            mod_date.text = self.modified_date.strftime(self.date_format)

        b = ET.fromstring(self.body)
        root.append(b)

        return ET.ElementTree(root)

converter_register = {
    'converter': BlogEntry,
    'type': 'blog',
    'required_meta': ['title', 'guid'],
}
