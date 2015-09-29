import requests
import sys

from bs4 import BeautifulSoup

from models import search_result


def search(name=''):
    # search query GET params
    url = 'http://web.worldbank.org/external/default/main'
    results = []

    # perform search query
    # http://web.worldbank.org/external/default/main?theSitePK=84266&contentMDK=64069844&menuPK=116730&pagePK=64148989&piPK=64148984
    params = {
        'theSitePK': 84266,
        'contentMDK': 64069844,
        'menuPK': 116730,
        'pagePK': 64148989,
        'piPK': 64148984,
    }
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
        parsed_result = search_result.copy()
        parsed_result['site'] = 'worldbank'
        parsed_result['name'] = parsed_row[0]
        parsed_result['country'] = parsed_row[2]
        parsed_result['address'] = parsed_row[1]
        if not name.lower() in parsed_result['name'].lower():
            continue
        results.append(parsed_result)

    return results

if __name__ == '__main__':
    print search(name='HEAVY')
    print search(name='heavy')
    print search(name='test')
