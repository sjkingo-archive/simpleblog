from markdown import Markdown

def parse_markdown(body):
    md = Markdown(safe_mode=True, output_format='xhtml')
    return md.convert(body)

filter_register = {
    'callback': parse_markdown
}
