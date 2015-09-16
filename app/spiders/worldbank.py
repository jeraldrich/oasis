import requests
import sys

from bs4 import BeautifulSoup

from models import search_result


def search(name=''):
    # search query GET params
    url = 'http://web.worldbank.org/external/default/main'
    params = {
        'pagePK': 64148989,
        'piPK': 64148984,
        'theSitePK': 84266,
        'contentMDK': 64069844,
        'querycontentMDK': 64069700,
        'sup_name': name,
        'supp_country': '',
    }

    # perform search query
    resp = requests.get(
        url,
        params=params,
    )
    if resp.status_code != 200: 
        print "worldbank search failed"
        print 'resp is ...'
        print resp.text
        return []

    # parse results
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'summary':'List of Debarred Firms'})
    rows = table.find_all('tr')

    # filter out non-relevant table rows
    rows = rows[2:]
    # process results
    columns = []
    results = []
    for i, row in enumerate(rows):
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        parsed_row = [ele for ele in cols if ele]
        # first row is table column names
        if i == 0:
            columns = parsed_row
            continue
        # junk row [u'From', u'To']
        if i == 1:
            continue
        # returns [u'No Matching Records found!']
        # if no match to search query
        if i == 2 and len(parsed_row) == 1:
            break
        result = ['worldbank', parsed_row[0],
                  parsed_row[2], parsed_row[1]]
        results.append(result)
    return results

if __name__ == '__main__':
    search(company_name='HEAVY')
    search(company_name='test')
    
