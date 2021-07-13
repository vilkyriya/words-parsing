import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.gastronom.ru/recipe/group/1132/recepty-napitkov-domashnie-napitki'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'accept': '*/*'}
HOST = 'https://www.gastronom.ru'
FILE = 'data/gastronom.csv'
COUNTER_NUM = 1

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def my_replace(item_text):
    alphabet = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ '
    signs = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~\n\r'
    item_modtext = ''.join([(' ' if ch in signs else ch) for ch in item_text])
    item_modtext = ''.join([ch for ch in item_modtext if ch in alphabet])
    item_modtext = item_modtext.lower()

    return item_modtext

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='recipe__step-text')

    drink = ''
    for item in items:
        drink += item.get_text() + " "
    drink = my_replace(drink)
    return drink

def get_main(html):
    global COUNTER_NUM
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('article', class_='material-anons col-sm-4 col-ms-12')

    drinks = []
    for item in items:
        if(item.find('a', class_='material-anons__img-wrapp js-fix')):
            html = get_html(HOST + item.find('a', class_='material-anons__img-wrapp js-fix').get('href'))
            drinks.append({
                'id': COUNTER_NUM,
                "recept": get_content(html.text)
            })
            COUNTER_NUM += 1

    return drinks

def save_file(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Номер', 'Рецепт'])
        for item in items:
            writer.writerow([item['id'], item['recept']])

def parse():
    # URL = input('Введите URL: ')
    # URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        drinks = []

        pages_count = 35
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            drinks.extend(get_main(html.text))

        save_file(drinks, FILE)
        print(f'Получено {len(drinks)} рецептов')
        # os.startfile(FILE)
    else:
        print('Error')

parse()
