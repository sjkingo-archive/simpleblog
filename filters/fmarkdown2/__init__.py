import markdown2

def parse_markdown(body):
    md = markdown2.Markdown()
    return md.convert(body)

filter_register = {
    'enabled': True,
    'callback': parse_markdown,
    'apply_to': 'entry_body',
}
