#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

LANGUAGES = ["C++", "C#", "PHP", "HTML", "PYTHON", "DJANGO", "JAVA", "SQL", "DELPHI", "PASCAL", "JOOMLA", "CSS"]
TITLE = 'title'
COST = 'cost'
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
        costs = row.find_all('div', class_ = 'b-vacancy-list-salary')
        skills = row.find_all('div', class_ = 'search-result-item__snippet')
        for i in range(len(titles)):
            title = titles[i].a.text
            skill = skills[i].text
            for language in LANGUAGES:
                if title.find(language) is not -1 and title not in works:
                    if i < len(costs):
                        if costs[i].meta.text is not None:
                            cost = costs[i].meta.text
                        else:
                            cost = None
                        works.append({
                            TITLE: title,
                            COST: cost,
                            SKILL: skill
                        })
        return works

def handling(page):
    """
    Обработка информации
    """
    return page

def main():
    page = []
    for i in range(51):
        handling(parse(get_html('https://hh.ru/search/vacancy?text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&area=' + str(i))))

main()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
