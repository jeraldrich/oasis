import requests
import sys

from bs4 import BeautifulSoup

from models import search_result


base_url = 'https://www.cia.gov/library/publications/world-leaders-1/'

# search page starts with https://www.cia.gov/library/publications/world-leaders-1/ 
# search for person name for all country list in cosCountryList nav
def search(name=''):
    results = []

    # perform search query for first page
    resp = requests.get(base_url)
    if resp.status_code != 200: 
        print 'cia search failed'
        print 'resp is ...'
        print resp.text
        return []
    parsed_results = parse_results(resp.text, name)
    if parsed_results:
        results += parsed_results
    
    return results


def parse_results(results, name):
    parsed_results = []

    soup = BeautifulSoup(results, "lxml")
    countries_ul = soup.findAll("ul", {"id" : "cosCountryList"})
    if not countries_ul: 
        return False
    for ul in countries_ul:
        for li in ul.findAll('li'):
            link = li.findAll('a', href=True)
            for l in link:
                href = l['href']
                country_url = "{}{}".format(
                    base_url,
                    href,
                )
                resp = requests.get(country_url)
                if resp.status_code != 200: 
                    print 'get country_url failed: {}'.format(
                        country_url,
                    )
                    print 'resp is ...'
                    print resp.text
                    return []
                #print resp.text
                # now parse country table result
                soup = BeautifulSoup(resp.text, "lxml")
                country_data = soup.findAll("span", {"class": "cos_name"})
                for person in country_data:
                    person_name = person.text.strip()
                    if name.lower() in person_name.lower():
                        parsed_result = search_result.copy()
                        parsed_result['site'] = 'cia'
                        parsed_result['name'] = person_name
                        parsed_result['country'] = country_url
                        parsed_results.append(parsed_result)
    return parsed_results


    #    country_name = country.text.strip()
    #   if not country_name:
    #        continue
    #    if not name.lower() in parsed_name.lower():
    #        continue
    #    parsed_result = search_result.copy()
    #    parsed_result['site'] = 'interpol'
    #    parsed_result['name'] = parsed_name
    #    parsed_results.append(parsed_result)

    #return parsed_results


if __name__ == '__main__':
    print search(name='HAMAD')
