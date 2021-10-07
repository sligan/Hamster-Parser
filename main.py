import csv

from bs4 import BeautifulSoup
import requests

URL = 'https://www.avito.ru/moskva/drugie_zhivotnye/gryzuny-ASgBAgICAUSyA8wV?cd=1&q=%D1%85%D0%BE%D0%BC%D1%8F%D0%BA'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.71 Safari/537.36', 'accept': '*/*'}
HOST = 'https://avito.ru'
FILE = 'hamsters.csv'


def save_file(items, path):
    with open(path, 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Цена', 'Метро', 'Когда выставлено'])
        for item in items:
            writer.writerow([item['name'], item['link'], item['price'], item['metro'], item['when']])


def get_html(url, params=None):
    r = requests.get(url=URL, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-JJq_j')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='iva-item-root-Nj_hb photo-slider-slider-_PvpN iva-item-list-H_dpX '
                                 'iva-item-redesign-nV4C4 iva-item-responsive-gIKjW items-item-My3ih '
                                 'items-listItem-Gd1jN js-catalog-item-enum')

    hamsters = []
    for item in items:
        hamsters.append({
            'name': item.find('div', class_='iva-item-titleStep-_CxvN').get_text(),
            'link': HOST + item.find('a', class_='link-link-MbQDP link-design-default-_nSbv title-root-j7cja '
                                                 'iva-item-title-_qCwt title-listRedesign-XHq38 '
                                                 'title-root_maxHeight-SXHes').get('href'),
            'price': item.find('span', class_='price-text-E1Y7h text-text-LurtD text-size-s-BxGpL').get_text().replace(
                '\xa0', '').replace('₽', 'Р'),
            'metro': item.find('div', class_='geo-root-H3eWU iva-item-geo-g3iIJ').get_text().replace('\xa0', ''),
            'when': item.find('div', class_='date-text-VwmJG text-text-LurtD text-size-s-BxGpL '
                                            'text-color-noaccent-P1Rfs').get_text()
        })
    return hamsters


def get_parse():
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        hamsters = []
        for page in range(1, pages_count + 1):
            print(f'Страница {page} из {pages_count}...')
            html = get_html(URL, params={'p': page})
            hamsters.extend(get_content(html.text))
        print(hamsters)
        save_file(hamsters, FILE)
    else:
        print('Error')


if __name__ == '__main__':
    get_parse()
