import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://namenu.ru/recipes-show_sub_category/id/46'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'accept': '*/*'}
HOST = 'https://namenu.ru/'
FILE = 'data/namenu.csv'
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
    item = soup.find('div', itemprop='recipeInstructions')
    drink = item.get_text()
    drink = my_replace(drink)
    return drink

def get_main(html):
    global COUNTER_NUM
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block')

    drinks = []
    for item in items:
        html = get_html(HOST + item.find('h4').find_next('a').get('href'))
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
        html = get_html(URL)
        pages_count = 12

        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL + '/page/' + str(page))
            drinks.extend(get_main(html.text))

        save_file(drinks, FILE)
        print(f'Получено {len(drinks)} рецептов')
    else:
        print('Error')

parse()
