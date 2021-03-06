import requests
import sys

from bs4 import BeautifulSoup

from models import search_result


base_url = 'http://www.interpol.int/notice/search/une'

# search page starts with http://www.interpol.int/notice/search/une
# paginated result = http://www.interpol.int/notice/search/une/(offset)/9
# http://www.interpol.int/notice/search/une/(offset)/9*2..9*3...9*4
# get all paginated results until no more results
# then search for person
def search(name=''):
    results = []

    # perform search query for first page
    resp = requests.get(base_url)
    if resp.status_code != 200: 
        print 'interpol search failed'
        print 'resp is ...'
        print resp.text
        return []
    parsed_results = parse_results(resp.text, name)
    if parsed_results:
        results += parsed_results
    
    # scrape all paginated pages
    for i in range(1, 100):
        page = i*9
        paginated_url = "{}/(offset)/{}".format(
            base_url,
            page,
        )
        resp = requests.get(paginated_url)
        if resp.status_code != 200: 
            print 'interpol paginated search failed'
            print 'resp is ...'
            print resp.text
            return []
        parsed_results = parse_results(resp.text, name)
        # if False is returned, we have gone beyond max
        # pagination
        if parsed_results == False:
            break
        if parsed_results:
            results += parsed_results

    return results


def parse_results(results, name):
    parsed_results = []

    soup = BeautifulSoup(results, "lxml")
    spans = soup.findAll("span", {"class" : "titre"})
    if not spans:
        return False

    for i, span in enumerate(spans):
        parsed_name = span.text.strip()
        if not parsed_name:
            continue
        if not name.lower() in parsed_name.lower():
            continue
        parsed_result = search_result.copy()
        parsed_result['site'] = 'interpol'
        parsed_result['name'] = parsed_name
        parsed_results.append(parsed_result)

    return parsed_results


if __name__ == '__main__':
    print search(name='ABDALLAH')
    print search(name='abdallah')
    print search(name='fred')
    
