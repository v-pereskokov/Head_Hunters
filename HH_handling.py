#!/usr/bin/env python3

import csv
import HH_parser

LANGUAGES = ["C++", " C ", "C#", "PHP", "HTML", "PYTHON", "DJANGO", "JAVA ", "JAVASCRIPT", "MYSQL", "DELPHI", "PASCAL",
             "JOOMLA", "CSS", "PERL", "1C", "RUBY", " GO ", "GOLANG", "RUST", "SWIFT", "OBJECTIVE C", "LINUX",
             "BASIC", "IOS"]
LANGUAGE = 'language'
TITLE = 'title'
PRICE = 'price'
MAX_PRICE = 'max_price'
MIN_PRICE = 'min_price'
MID_PRICE = 'mid_price'
SKILL = 'skill'
COUNT = 'count'


def date_to_string(date):
    return str(date['day']) + '.' + str(date['month']) + '.' + str(date['year'])


def save_language(languages, jobs, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ('Область', 'Средняя зарплата', 'Минимальная зарплата', 'Максимальная зарплата',
             'Число вакансий(в период с ' + date_to_string(jobs[len(jobs) - 1]['date']) + ' по ' + date_to_string(
                 jobs[0]['date']) + ')'))
        writer.writerows(
            (language[LANGUAGE], language[MID_PRICE], language[MIN_PRICE], language[MAX_PRICE], language[COUNT]) for
            language in languages)


def middle(prices):
    mid = 0
    for i in prices:
        mid += i
    return mid // len(prices)


def write_language(jobs):
    languages = []
    count = 0
    for language in LANGUAGES:
        prices = []
        for i in range(len(jobs)):
            if (jobs[i][TITLE] + ' ' + jobs[i][SKILL]).upper().find(language) is not -1:
                count += 1
                if jobs[i][PRICE] is not None:
                    prices.append(int(jobs[i][PRICE]))
        if len(prices) is not 0:
            add = {
                LANGUAGE: language,
                PRICE: prices,
                MID_PRICE: middle(prices),
                MIN_PRICE: min(prices),
                MAX_PRICE: max(prices),
                COUNT: count
            }
            if add not in languages:
                languages.append(add)
        count = 0
    languages.sort(key=lambda x: x[COUNT], reverse=True)
    return languages


def handling():
    jobs = HH_parser.parsing()
    print('Handling languages...')
    languages = write_language(jobs)
    print('Saving languages...')
    save_language(languages, jobs, 'languages.csv')
