from BeautifulSoup import BeautifulSoup as bs

def prettify_html(s):
    d = bs(s)
    return d.prettify()

filter_register = {
    'enabled': True,
    'callback': prettify_html,
    'apply_to': 'html_file',
}
