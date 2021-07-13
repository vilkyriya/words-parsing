import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://gotovim-doma.ru/category/55-napitki'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'accept': '*/*'}
HOST = 'https://gotovim-doma.ru'
FILE = 'data/gotovim_doma.csv'
COUNTER_NUM = 1

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('li', class_='last').find_next('a').get_text()
    print(pagination)
    if pagination:
        return int(pagination)
    else:
        return 1


def my_replace(item_text):
    alphabet = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ '
    signs = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~\n\r'
    item_modtext = ''.join([(' ' if ch in signs else ch) for ch in item_text])
    item_modtext = ''.join([ch for ch in item_modtext if ch in alphabet])
    item_modtext = item_modtext.lower()

    return item_modtext

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='step')

    drink = ''
    for item in items:
        drink += item.find('p').get_text() + " "
    drink = my_replace(drink)
    return drink

def get_main(html):
    global COUNTER_NUM
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='recept-item-img')

    drinks = []
    for item in items:
        html = get_html(HOST + item.find('a').get('href'))
        drinks.append({
            'id': COUNTER_NUM,
            "recept": get_content(html.text)
        })
        COUNTER_NUM += 1
    # print(drinks)
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

        pages_count = get_pages_count(html.text)
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