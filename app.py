import json
import urllib.parse

import colorama
import requests
import xmltodict
from bs4 import BeautifulSoup
from colorama import Fore, Style


base_url = 'https://zillow.com/webservice'
colorama.init()

with open('config.json') as f:
    cfg = json.load(f)

ZWSID = cfg.get('ZWSID')
city, state = cfg.get('neighborhood').split(', ')
filters = cfg.get('filters', {})

params = {
    'zws-id': ZWSID,
    'city': city,
    'state': state
}
r = requests.get(f'{base_url}/GetRegionChildren.htm', params=params)
resp = xmltodict.parse(r.text, process_namespaces=True)['http://www.zillow.com/static/xsd/RegionChildren.xsd:regionchildren']
if r.status_code != 200:
    raise ValueError(resp['message'])
data = resp['response']

params = {
    "pagination": {},
    "mapBounds": {
        "west": float(data['region']['longitude']) - 0.5,
        "east": float(data['region']['longitude']) + 0.5,
        "south": float(data['region']['latitude']) - 0.5,
        "north": float(data['region']['latitude']) + 0.5
    },
    "usersSearchTerm": city + ' ' + state,
    "regionSelection": [
        {
            "regionId": int(data['region']['id']),
            "regionType": 6
        }
    ],
    "isMapVisible": True,
    "mapZoom": 12,
    "filterState": {
        "sortSelection": {
            "value": filters.get('sort', 'days')
        },
        "isForRent": {
            "value": filters.get('rent_max', 0) != -1
        },
        "enableSchools": {
            "value": False
        }
    },
    "isListVisible": True
}

# Filters
if filters.get('price_max') != 0:
    params['filterState']['price'] = {'min': filters.get('price_min'), 'max': filters.get('price_max')}

if filters.get('rent_max') != 0:
    params['filterState']['monthlyPayment'] = {'min': filters.get('rent_min'), 'max': filters.get('rent_max')}

beds = filters.get('beds')
if beds != '-1':
    params['filterState']['beds'] = {'min': int(beds[0])}
    if not beds.endswith('+'):
        params['filterState']['beds']['max'] = int(beds[0])

baths = filters.get('baths')
if baths != 0:
    params['filterState']['baths'] = {'min': baths}

if filters.get('sqft_max') != 0:
    params['filterState']['sqft'] = {'min': filters.get('sqft_min'), 'max': filters.get('sqft_max')}

# So we don't look like a robot
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}

url = f"https://zillow.com/{city.replace(' ', '-').lower()}-{state.lower()}/?searchQueryState={urllib.parse.quote(str(params))}"
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, 'lxml')
listings = soup.find('ul', class_='photo-cards').find_all('li', recursive=False)
print('-' * 100)

for i in listings:
    # print(i.prettify())
    try:
        address = i.article.a.h3.text
        price = i.find('div', class_='list-card-price').text
        rent = i.find('div', class_='list-card-type').text
        print(f'{rent} at {price} - {address}')

        is_renting = False
        if 'rent' in rent:
            is_renting = True
    except:
        # Sadly the 3rd result is "Loading" every time
        pass
    else:
        params = {
            'zws-id': ZWSID,
            'address': address,
            'citystatezip': address[-5:],
            'rentzestimate': True
        }
        r = requests.get(f'{base_url}/GetSearchResults.htm', params=params)
        resp = xmltodict.parse(r.text, process_namespaces=True)['http://www.zillow.com/static/xsd/SearchResults.xsd:searchresults']
        if r.status_code != 200:
            raise ValueError(resp['message'])
        data = resp['response']['results']['result']
        try:
            z = data['zestimate']
        except TypeError:
            data = data[0]
            z = data['zestimate']
        if data.get('rentzestimate') and is_renting:
            z = data['rentzestimate']

        try:
            num_bars = 25
            lowest_value = int(z['valuationRange']['low']['#text'])
            highest_value = int(z['valuationRange']['high']['#text'])
            current_value = int(z['amount']['#text'])
            price = int(price.replace(',', '').replace('$', '').replace('/mo', ''))
            relative_value = price - current_value
            higher_than_zestimate = Fore.GREEN
            if relative_value > 0:
                higher_than_zestimate = f'{Fore.RED}+'

            if price < lowest_value:
                pos = -1
            elif price > highest_value:
                pos = num_bars
            else:
                dash_value = (highest_value - lowest_value) / num_bars
                pos = round((price - lowest_value) / dash_value) - 1

            print(f"Current Zestimate: ${current_value} (Last updated: {z['last-updated']})")
            print(f"Zestimate change in the last 30 days: ${z['valueChange']['#text']}")
            print(f'List Price relative to Zestimate: {higher_than_zestimate}{relative_value}{Style.RESET_ALL}')
            print(" " * (18 + pos) + "v")
            print(f"Valuation Range: |{'=' * num_bars}|")
            print(f"{' ' * 14}${z['valuationRange']['low']['#text']}{' ' * (num_bars - 6)}${z['valuationRange']['high']['#text']}")
        except KeyError:
            print('No data')
        finally:
            print('\nWant to read more?')
            print(f"Home Details: {data['links']['homedetails']}")
            print(f"Comparable Homes: {data['links']['comparables']}")
            print('-' * 100)