from BeautifulSoup import BeautifulSoup as bs

def prettify_html(s):
    d = bs(s)
    return d.prettify()

filter_register = {
    'callback': prettify_html,
    'when': 'end'
}
