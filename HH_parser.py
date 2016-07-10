#!/usr/bin/env python3

import csv
import urllib.request as urllib
from datetime import datetime
from bs4 import BeautifulSoup
import currency_parser as cur_pars

URL_PREMIUM = \
    'https://hh.ru/search/vacancy?text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&area='
URL_STANDART = 'https://hh.ru/search/vacancy?enable_snippets=true&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&search_field=name&clusters=true&page='
TITLE = 'title'
PRICE = 'price'
SKILL = 'skill'
DATE = 'date'
YEAR = 'year'
MONTH = 'month'
DAY = 'day'
months = ['янвяр', 'феврал', 'март', 'апрел', 'ма', 'июн', 'июл', 'август', 'сентябр', 'октябр', 'ноябр',
          'декабр']


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
        if char in ['U', 'E', 'K', 'г']:
            index = price.index(char)
            for i in range(index, index + 3):
                currency += price[i]
            break
        elif char == 'е':
            index = price.index(char) - 1
            for i in range(index, index + 3):
                currency += price[i]
            break
    return currency


def save_jobs(jobs, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Название', 'Цена', 'Требование', 'Дата(Д/М/Г)'))
        writer.writerows(
            (job[TITLE], job[PRICE], job[SKILL],
             (str(job[DATE][DAY]) + '.' + str(job[DATE][MONTH]) + '.' + str(job[DATE][YEAR]))) for job in jobs)


def calculation(price):
    currencys = cur_pars.parse()
    currency = which_currency(price)
    price = clear_price(price)
    for i in range(len(currencys)):
        if currency == currencys[i]['name']:
            price = int(price) * int(float(currencys[i]['currency'])) / int(currencys[i]['unit'])
            break
    return int(price)


def string_to_date(date):
    month = ''
    day = ''
    for i in range(len(date)):
        if date[i].isdigit():
            while date[i].isdigit():
                day += date[i]
                i += 1
            i += 1
        if date[i].isalpha():
            for j in range(i, len(date) - 1):
                month += date[i]
                i += 1
            break
    for month_ in months:
        if month_ == month.lower():
            month = months.index(month_) + 1
            break
    result = {
        YEAR: datetime.now().year,
        MONTH: month,
        DAY: int(day)
    }
    return result


def reading_html(html, jobs, _class):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='l l_auto')
    all_items = table.find('div', class_='search-result') \
        .find_all('div', class_=_class)
    for i in range(len(all_items)):
        if all_items[i].find('div', class_='b-vacancy-list-salary') is not None:
            price = all_items[i].find('div', class_='b-vacancy-list-salary').meta.text
            price = calculation(price)
        else:
            price = None
        title = all_items[i].find('div', class_='search-result-item__head').a.text
        skills = all_items[i].find_all('div', class_='search-result-item__snippet')
        skill = skills[0].text + ' ' + skills[1].text
        date = all_items[i].find('span', class_='b-vacancy-list-date').text
        job = {
            TITLE: title,
            PRICE: price,
            SKILL: skill,
            DATE: string_to_date(date)
        }
        if job not in jobs:
            jobs.append(job)
    jobs.sort(key=lambda x: x[DATE][DAY], reverse=True)


def parsing():
    jobs = []
    print('Parsing jobs...')
    for page in range(10):
        reading_html(get_html(URL_PREMIUM + str(page)), jobs,
                     'search-result-item search-result-item_premium  search-result-item_premium')
    for page in range(99):
        reading_html(get_html(URL_STANDART + str(page)), jobs,
                     'search-result-item search-result-item_standard ')
    print('Saving jobs...')
    save_jobs(jobs, 'all_jobs.csv')
    return jobs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
