#!/usr/bin/env python3

import csv
import urllib.request
from bs4 import BeautifulSoup

URL = 'https://hh.ru/search/vacancy?text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&area='
LANGUAGES = ["C++", "C#", "PHP", "HTML", "PYTHON", "DJANGO", "JAVA", "SQL", "DELPHI", "PASCAL", "JOOMLA", "CSS"]
TITLE = 'title'
PRICE = 'price'
SKILL = 'skill'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', class_ = 'l l_auto HH-StickyParentAreaResizer-Content')
    works = []
    for row in table.find_all('tr'):
        titles = row.find_all('div', class_ = 'search-result-item__head')
        prices = row.find_all('div', class_ = 'b-vacancy-list-salary')
        skills = row.find_all('div', class_ = 'search-result-item__snippet')
        for i in range(len(titles)):
            title = titles[i].a.text
            skill = skills[i].text
            for language in LANGUAGES:
                if title.find(language) is not -1 and title not in works:
                    if i < len(prices):
                        if prices[i].meta.text is not None:
                            price = prices[i].meta.text
                        else:
                            price = None
                        works.append({
                            TITLE: title,
                            PRICE: price,
                            SKILL: skill
                        })
        return works

def save(works, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Проект', 'Цена', 'Требования'))
        writer.writerows(
            (work[TITLE], work[PRICE], work[SKILL]) for work in works)

def main():
    works = []
    for page in range(51):
        print('Parsing %d%% (%d/%d)' % ((page + 1)/ 51 * 100, page + 1, 51))
        works.extend(parse(get_html(URL + str(page))))
    print('Saving...')
    save(works, 'works.csv')


main()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
