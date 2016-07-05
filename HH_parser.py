#!/usr/bin/env python3

import csv
import urllib.request as urllib
from bs4 import BeautifulSoup
import currency_parser as cur_pars

URL_PREMIUM = 'https://hh.ru/search/vacancy?text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&area='
URL_STANDART = 'https://hh.ru/search/vacancy?enable_snippets=true&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&search_field=name&clusters=true&page='
TITLE = 'title'
PRICE = 'price'
SKILL = 'skill'


def get_html(url):
    return urllib.urlopen(url).read()


def clear_price(price):
    result_price = ''
    for char in price:
        if char.isdigit():
            result_price += char
        elif char == '-':
            break
    return result_price


def which_currency(price):
    currency = ''
    for char in price:
        if char == 'U' or char == 'E' or char == 'K' or char == 'г':
            index = price.index(char)
            for i in range(index, index + 3):
                currency += price[i]
            break
    return currency


def calculation(price):
    currencys = cur_pars.parse()
    currency = which_currency(price)
    price = clear_price(price)
    for i in range(len(currencys)):
        if currency == currencys[i]['name']:
            price = int(price) * int(float(currencys[i]['currency']))
            break
    return price


def parse(html, jobs, _class):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='l l_auto')
    all_items = table.find('div', class_='search-result') \
        .find_all('div', class_=_class)
    for i in range(len(all_items)):
        title = all_items[i].find('div', class_='search-result-item__head').a.text
        if all_items[i].find('div', class_='b-vacancy-list-salary') is not None:
            price = all_items[i].find('div', class_='b-vacancy-list-salary').meta.text
        else:
            price = None
        if price is not None:
            price = calculation(price)
        skills = all_items[i].find_all('div', class_='search-result-item__snippet')
        skill = skills[0].text + ' ' + skills[1].text
        job = {
            TITLE: title,
            PRICE: price,
            SKILL: skill
        }
        if job not in jobs:
            jobs.append(job)
    return jobs


def save(jobs, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Название', 'Цена', 'Требоавние'))
        writer.writerows(
            (job[TITLE], job[PRICE], job[SKILL]) for job in jobs)


def parsing():
    jobs = []
    print('Parsing jobs...')
    for page in range(10):
        parse(get_html(URL_PREMIUM + str(page)), jobs,
              'search-result-item search-result-item_premium  search-result-item_premium')
    for page in range(99):
        parse(get_html(URL_STANDART + str(page)), jobs,
              'search-result-item search-result-item_standard ')
    print('Saving jobs...')
    save(jobs, 'jobs.csv')
    return jobs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
