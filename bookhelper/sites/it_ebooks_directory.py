from lxml import html, etree
import re
from bookhelper import FormatException, ElementNames


def extract_data(content):

    try:
        title = html.fromstring(content).xpath('.//h1/text()')
        if not title or len(title)==0:
            msg = 'Title not found in HTML'
            raise FormatException(msg)
        else:
            title = title[0].strip()
            if len(title) == 0:
                raise FormatException('Title has 0 length')

            print('Successfully got title [%s]' % (title,))
    except Exception as e:
        print('Warning:', e)
        title = ''

    tables = html.fromstring(content).xpath('.//table[@class="table table-bordered"]')

    if len(tables) == 0:
        print("query for tables returned no element")
        return {ElementNames.TITLE: '', ElementNames.AUTHOR: '', ElementNames.YEAR: '', \
                ElementNames.DESCRIPTION: ''}

    author = tables[0].xpath('./tr[3]/td[2]/a/text()')
    try:
        if not author or len(author)==0:
            msg = 'Author not found'
            raise FormatException(msg)
        else:
            author = author[0].strip()
            if len(author) == 0:
                raise FormatException('Author has 0 length')
            print('Successfully got author [%s]' % (author,))
    except Exception as e:
        print('Warning:', e)
        author = ''

    year = ''
    try:
        year = tables[1].xpath('./tr[2]/td[2]/text()')
        if year is None or len(year) == 0:
            raise FormatException('Year not found in HTML')
        year = year[0]
        regexp = re.compile(r'^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+[0-3][0-9]\s+(19[0-9]{2}|20[0,1][0-9])$')
        res = regexp.search(year)
        if res:
            year = res.groups()[0]
            print('Date successfully retrieved %s' % year)
        if not year or len(year) == 0:
            msg = 'Error retrieving year in [%s]' % str
            raise FormatException(msg)
    except Exception as e:
        print('Warning:', e)
        year = ''

    descr = html.fromstring(content).xpath('//div[@class="row-fluid"][descendant::h4/text()="Book Description:"]/following-sibling::div[1]/div/text()')
    try:
        if descr is None or len(descr) == 0:
            raise FormatException('Description not found in HTML')
        descr = descr[0].strip()
        if len(descr) == 0:
            raise FormatException('Description has 0 length')
    except Exception as e:
        print('Warning:',e)
        descr = ''
    return {ElementNames.TITLE: title.strip(), ElementNames.AUTHOR: author.strip(), ElementNames.YEAR: year, \
                ElementNames.DESCRIPTION: descr}


if __name__=="__main__":
    url = 'http://it-ebooks.directory/book-1430249080.html'
    from bookhelper.sites.http_request import get_http_content
    content = get_http_content(url)
    """
    content = ''
    with open('content.html','rb') as frd:
        content = frd.read()
    print(content[:500])
    """
    print(extract_data(content))