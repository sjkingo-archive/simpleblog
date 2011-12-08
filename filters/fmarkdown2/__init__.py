import markdown2

def parse_markdown(body):
    md = markdown2.Markdown()
    return md.convert(body)

filter_register = {
    'callback': parse_markdown,
    'when': 'start'
}
