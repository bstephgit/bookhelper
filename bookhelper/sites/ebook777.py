from lxml import html, etree
import re
from bookhelper import FormatException, ElementNames


def extract_data(content):
    title = html.fromstring(content).xpath('.//h1[@class="title"]/text()')[0].strip()
    try:
        #str = node.xpath('b/text()')
        if not title or len(title)==0:
            msg = 'Error retrieving title'
            raise FormatException(msg)
        else:
            print('Successfully got title [%s]' % (title,))
    except Exception as e:
        print('Warning:', e)

    author = html.fromstring(content).xpath('.//table/tr[1]/td[3]/text()')[0].strip()
    try:
        #str = node.xpath('b/text()')
        if not author or len(author)==0:
            msg = 'Error retrieving author'
            raise FormatException(msg)
        else:
            print('Successfully got author [%s]' % (author,))
    except Exception as e:
        print('Warning:', e)

    year = ''
    try:
        year = html.fromstring(content).xpath('.//table/tr[4]/td[2]/text()')[0].strip()
        regexp = re.compile(r'^19[0-9]{2}|20[0,1][0-9]$')
        res = regexp.search(year)
        if res:
            print('Date successfully retrieved %s' % year)
        if not year or len(year) == 0:
            msg = 'Error retrieving year in [%s]' % str
            raise FormatException(msg)
    except Exception as e:
        print('Warning:', e)

    descr = ''
    siblings = html.fromstring(content).xpath('//h3[contains(text(),"Book Description:")=true]/following-sibling::*')
    for item in siblings:
        if item.tag == 'script':
            continue 
        if item.text:
            txt = etree.tostring(item, encoding='UTF-8').replace(b'\n', b'').decode('utf-8').strip()
            descr += txt
        #print('description=%s',descr)

    return {ElementNames.TITLE: title.strip(), ElementNames.AUTHOR: author.strip(), ElementNames.YEAR: year, \
                ElementNames.DESCRIPTION: descr}


if __name__=="__main__":
    url = 'http://www.ebook777.com/game-theory-applications-game-theoretic-models-mathematical-ecology/'
    from bookhelper.sites.http_request import get_http_content
    content = get_http_content(url)
    print(content[:100])
    with open('content.html','wb') as fwr:
        fwr.write(content)
    print(extract_data(content))