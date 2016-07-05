#!/usr/bin/env python3

import csv
import HH_parser

LANGUAGES = ["C++", "C#", "PHP", "HTML", "PYTHON", "DJANGO", "JAVA", "JAVASCRIPT", "MYSQL", "SQL", "DELPHI", "PASCAL", "JOOMLA", "CSS", "PERL",
             "1C", "RUBY", "GO", "GOLANG", "RUST", "SWIFT", "OBJECTIVE C", "COCOA", "LINUX", "BASIC", "IOS"]
LANGUAGE = 'language'
TITLE = 'title'
PRICE = 'price'
SKILL = 'skill'


def save_language(languages, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Область', 'Средняя зарплата'))
        writer.writerows(
            (language[LANGUAGE], language[PRICE]) for language in languages)


def handling():
    jobs = HH_parser.parsing()
    print('Handling languages...')
    languages = []
    language = ''
    price = 0
    count = 0
    is_work = False
    for lang in LANGUAGES:
        for i in range(len(jobs)):
            if jobs[i][PRICE] is not None:
                if jobs[i][TITLE].upper().find(lang) is not -1 or jobs[i][SKILL].upper().find(lang) is not -1:
                    if not is_work:
                        language = lang
                        price = int(jobs[i][PRICE])
                        count += 1
                        is_work = True
                    else:
                        price += int(jobs[i][PRICE])
                        count += 1
        add_language = {
            LANGUAGE: language,
            PRICE: price // count
        }
        if add_language not in languages:
            languages.append(add_language)
        is_work = False
    print('Saving languages...')
    save_language(languages, 'languages.csv')
