"""

    MIT License

    Copyright (c) 2018 - 2023 Shrey Dabhi

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
}


def indices(category):
    cat = {
        "market_cap/broad": "1,2",
        "sector_and_industry": "2,2",
        "thematics": "3,2",
        "strategy": "4,2",
        "sustainability": "5,2",
        "volatility": "6,1",
        "composite": "7,1",
        "government": "8,1",
        "corporate": "9,1",
        "money_market": "10,1"
    }
    try:
        ddl_category = cat[category]
    except KeyError:
        print('''
### Invalid category ###
Use one of the categories mentioned below:

market_cap/broad
sector_and_industry
thematics
strategy
sustainability
volatility
composite
government
corporate
money_market
        ''')
        return
    baseurl = '''https://m.bseindia.com/IndicesView_New.aspx'''
    res = requests.get(baseurl, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    options = {
        '__EVENTTARGET': 'ddl_Category',
        '__VIEWSTATEENCRYPTED': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATEGENERATOR': '162C96CD',
        'UcHeaderMenu1$txtGetQuote': '',
        '__EVENTVALIDATION': '',
        '__VIEWSTATE': ''
    }
    for input in soup("input"):
        try:
            if(input['type'] == "hidden"):
                if(input['id'] == '__VIEWSTATE'):
                    options['__VIEWSTATE'] = input['value']
                elif(input['id'] == '__EVENTVALIDATION'):
                    options['__EVENTVALIDATION'] = input['value']
        except KeyError:
            continue
    options['ddl_Category'] = ddl_category
    res = requests.post(url=baseurl, data=options, headers=headers)
    c = res.content
    soup = bs(c, "lxml")
    index_list = []
    for td in soup('td'):
        try:
            if(td['class'][0] == 'TTRow_left'):
                index = {}
                index['currentValue'] = td.next_sibling.string.strip()
                index['change'] = td.next_sibling.next_sibling.string.strip()
                index['pChange'] = td.next_sibling.next_sibling.next_sibling.string.strip()
                index['scripFlag'] = td.a['href'].strip().split('=')[1]
                index['name'] = td.a.string.strip().replace(';', '')
                index_list.append(index)
        except KeyError:
            continue
    results = {}
    for span in soup("span", id="inddate"):
        results['updatedOn'] = span.string[6:].split('|')[0].strip()
    results['indices'] = index_list
    return results
