#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

URL = 'http://www.banki.ru/products/currency/cb/'
NAME = 'name'
CURRENCY = 'currency'


def get_html(url):
    return urllib.request.urlopen(url).read()


def parse():
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table',
                      class_='standard-table standard-table--row-highlight')
    currencys = []
    for i in [0, 1, 12, 14, 26]:
        all = table.find('tbody').find_all('tr')[i]
        name = all.find_all('td')[0].text
        currency = all.find_all('td')[3].text
        result_name = ''
        result_currency = ''
        if i != 26:
            for j in range(12, 15):
                result_name += name[j]
        else:
            result_name = 'грн'
        for k in range(6, 13):
            result_currency += currency[k]
        currencys.append({
            NAME: result_name,
            CURRENCY: result_currency
         })
    return currencys
