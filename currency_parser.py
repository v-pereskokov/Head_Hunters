#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

URL = 'http://www.banki.ru/products/currency/cb/'
NAME = 'name'
CURRENCY = 'currency'
UNIT = 'unit'


def get_html(url):
    return urllib.request.urlopen(url).read()


def parse():
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table',
                      class_='standard-table standard-table--row-highlight')
    currencys = []
    for i in [0, 1, 5, 12, 14, 26]:
        all = table.find('tbody').find_all('tr')[i].find_all('td')
        name = all[0].text
        currency = all[3].text
        unit = all[1].text
        result_name = ''
        if i == 5:
            result_name = 'бел'
        elif i == 26:
            result_name = 'грн'
        else:
            for j in range(12, 15):
                result_name += name[j]
        currencys.append({
            NAME: result_name,
            CURRENCY: float(currency),
            UNIT: int(unit)
        })
    return currencys
