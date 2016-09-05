#!/usr/bin/env python3

# Для http запроса
import urllib.request as urllib
# Даты
import datetime
# Для парсинга html разметки
from bs4 import BeautifulSoup
# sleep
import time
# Для записи данных в файл с расширением 'csv'
import csv
import threading
# 'Синонимы'
import defines


# Преобразование ко времени
def to_date(year, month, day):
    return datetime.datetime(year, month, day)


# Определяем дату последнего объявления
def search_days(days):
    delta = datetime.date.today() - datetime.timedelta(days=days)
    return to_date(int(str(delta)[:4]), int(str(delta)[5:7]), int(str(delta)[8:10]))


# Switch для y/n
def switch_y_n(case):
    switcher = {
        'y': True,
        'n': False
    }
    return switcher.get(case, False)    


# HTTP - запрос
def get_html(url):
    while True:
        try:
            with urllib.urlopen(url) as query:
                return query.read()
        except (urllib.socket.error, IOError) as e:
            print(e)
            print('Повторить подключение? y/n')
            enter = input()
            if not switch_y_n(enter):
                print('Попробуйте позднее...')
                break
            time.sleep(5)


# Преобразование месяца как строки в дату
def month_to_digit(month):
    month = month[:len(month) - 1]
    months = defines.months
    for month_ in months:
        if month_ == month.lower():
            return months.index(month_) + 1


# Перевод строки в дату
def string_to_date(date):
    month = ''
    day = ''
    year = ''
    i = 0
    # осторожно, быдлокод
    while True:
        if date[i].isdigit():
            day += date[i]
        else:
            break
        i += 1
    i += 1
    while True:
        if date[i].isalpha():
            month += date[i]
        else:
            break
        i += 1
    month = month_to_digit(month)
    i += 1
    year = date[i:]
    return datetime.datetime(int(year), month, int(day))


# Поиск id объявления
def find_id(string):
    return string[(string.find("id") + 3):]


# Разметка страницы
def B_soup(html, type='html.parser'):
    return BeautifulSoup(html, type)


# Проверка на одинаковые языки программирования
def check_languages(language, languages):
    # Исправить
    if language is "JAVASCRIPT" or language is "JS":
        if language in languages:
            return True
        else:
            return False
    elif language is "OBJECTIVE-C" or language is "OBJECTIVE C":
        if language in languages:
            return True
        else:
            return False
    else:
        return False


# Поиск языков программирования
def find_languages(description):
    languages = ''
    for language in defines.LANGUAGES:
        if description.upper().find(language) is not -1:
            languages += language + ' . '
    return languages[:len(languages) - 2]


# Исследования работы
def research_job(page, _date):
    soup = B_soup(get_html(page))
    all_items = soup.find('div', class_='HH-MainContent')
    title = all_items.find('h1', class_='title b-vacancy-title').text
    main_info = all_items.find('table', class_='l-content-3colums')
    price = main_info.find('td', class_='l-content-colum-1 b-v-info-content').text
    if price[0:2] != 'от':
        price = price[1:]
    location = main_info.find('td', class_='l-content-colum-2 b-v-info-content').text
    experience = main_info.find('td', class_='l-content-colum-3 b-v-info-content').text
    isadd = True
    date = ''
    languages = ''
    if all_items.find('table', class_='l-content-2colums b-vacancy-container') is not None:
        description = all_items.find('table', class_='l-content-2colums b-vacancy-container') \
            .find('div', class_='b-vacancy-desc-wrapper').text
        languages = find_languages(description)
        if len(languages) == 0:
            isadd = False
        date = all_items.find('table', class_='l-content-2colums b-vacancy-container') \
            .find('td', class_='l-content-colum-2').find('time', class_='vacancy-sidebar__publication-date').text
        date = string_to_date(date)
    else:
        # par1 - Продолжать ли просмотр других вакансий
        # par2 - Добавлять ли эту работу в общий список
        # par3 - Работа
        isadd = False
    is_continue = True
    print(date, _date)
    if date == _date:
        is_continue = False
    print('\n\n')
    return [is_continue, isadd, {
        defines.TITLE: title,
        defines.PRICE: price,
        defines.SKILL: languages,
        defines.DATE: date,
        defines.LOCATION: location,
        defines.EXPERIENCE: experience
    }]


# Обработка предложений
def query_handle(html, jobs, _date, _class):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='l l_auto')
    all_items = table.find('div', class_='search-result')\
        .find_all('div', class_=_class)
    for i in range(len(all_items)):
        id = all_items[i].select('a')
        print(defines.URL_VACANCY + find_id(str(id[0].attrs['href'])))
        result = research_job(defines.URL_VACANCY + find_id(str(id[0].attrs['href'])), _date)
        if not result[0]:
            return False
        if result[1]:
            job = result[2]
            if job not in jobs:
                jobs.append(job)
    return True


def parse(date, jobs, page, url, _class):
    return query_handle(get_html(url + str(page)), jobs,
                        date, _class)


# Сохранение всех предложений в таблицу в файл с расширением 'csv'
def save_jobs(jobs, path):
    with open(path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Название', 'ЗП', 'ЯП', 'Опыт', 'Город', 'Дата(Г/М/Д)'))
        writer.writerows(
            (job[defines.TITLE], job[defines.PRICE], job[defines.SKILL], job[defines.EXPERIENCE], job[defines.LOCATION],
             str(job[defines.DATE])[:11]) for job in jobs)


def parse_thread(date, jobs, url, _class):
    i = 0
    while parse(date, jobs, i, url,
                _class):
        i += 1
        print('page: ', i)
        if i == 99:
            break


# Обработка сайта hh.ru
def parsing(days, path, sort=True):
    jobs = []
    print('Обработка данных...\nПожалуйста подождите...')
    date = search_days(days)
    print(date)
    thread1 = threading.Thread(target=parse_thread, name='name1', args=[date, jobs, defines.URL, defines.PREMIUM_CLASS])
    thread2 = threading.Thread(target=parse_thread, name='name2', args=[date, jobs, defines.URL, defines.STANDARD_CLASS])
    thread3 = threading.Thread(target=parse_thread, name='name3', args=[date, jobs, defines.URL, defines.STANDARD_PLUS_CLASS])
    thread1.start()
    thread2.start()
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()

    # i = 0
    # while parse(date, jobs, i, defines.URL, ):
    #     i += 1
    #     print('stand: ', i)
    #     if i == 99:
    #         break
    # i = 0
    # while parse(date, jobs, i, defines.URL, ):
    #     i += 1
    #     print('stand_plus: ', i)
    #     if i == 99:
    #         break
    jobs.sort(key=lambda x: x[defines.DATE], reverse=sort)
    print('Сохранени данных...')
    save_jobs(jobs, path)
    print('Данные успешно сохранены!')
