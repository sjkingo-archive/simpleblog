from markdown import Markdown

def parse_markdown(body):
    print 'tomarkdown filter called with "%s"' % body
    md = Markdown(safe_mode=True, output_format='xhtml')
    return md.convert(body)

filter_callback = parse_markdown
