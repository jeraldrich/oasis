import requests
import sys

from bs4 import BeautifulSoup

from models import search_result


# search page starts with http://www.interpol.int/notice/search/une
# paginated result = http://www.interpol.int/notice/search/une/(offset)/9
# http://www.interpol.int/notice/search/une/(offset)/9*2..9*3...9*4
# get all paginated results until no more results
# then search for person
def search(name=''):
    base_url = 'http://www.interpol.int/notice/search/une'
    results = []

    # perform search query for first page
    resp = requests.get(base_url)
    if resp.status_code != 200: 
        print ""
        print 'resp is ...'
        print resp.text
        return []

    parsed_results = parse_results(resp.text)
    for r in parsed_results:
        if name.lower() in r['name'].lower():
            results.append([
                r['site'],
                r['name'],
                r['address'],
                r['country'],
            ])

    return results


def parse_results(results):
    parsed_results = []

    soup = BeautifulSoup(results, "lxml")
    spans = soup.findAll("span", {"class" : "titre"})

    for i, span in enumerate(spans):
        parsed_result = search_result.copy()
        parsed_result['site'] = 'interpol'
        parsed_name = span.text.strip()
        parsed_result['name'] = parsed_name
        parsed_results.append(parsed_result)

    return parsed_results


if __name__ == '__main__':
    print search(name='ABDALLAH')
    print search(name='abdallah')
    print search(name='fred')
    
