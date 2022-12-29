import requests
from bs4 import BeautifulSoup

URL = 'https://s1.otxatabanet.ru/'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36'
}


def get_html(url):
    req = requests.get(url=url, headers=HEADERS)
    return req


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="entry")
    game = []
    for item in items:
        date = item.find('div', class_='entry__info-categories')
        if date is None:
            continue
        card = {
            'image': URL + item.find('img').get('src'),
            'link': item.find('div', class_='entry__title h2').find('a').get('href'),
            'title': item.find('div', class_='entry__title h2').find('a').string,
            'date': item.find('div', class_='entry__info-categories').string
        }
        game.append(card)
    return game


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        game = []
        for i in range(1, 3):
            html = get_html(f"{URL}page/{i}/")
            current_page = get_data(html.text)
            game.extend(current_page)
        return game
    else:
        raise Exception("Bad request in parser!")
