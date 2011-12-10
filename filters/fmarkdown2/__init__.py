import markdown2

def parse_markdown(body):
    extras = ['code-friendly', 'smarty-pants']
    md = markdown2.Markdown(extras=extras)
    return md.convert(body)

filter_register = {
    'enabled': True,
    'callback': parse_markdown,
    'apply_to': 'entry_body',
}
