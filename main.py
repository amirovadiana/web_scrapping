import requests
import bs4
from fake_headers import Headers
from pprint import pprint


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def get_fake_headers():
    return Headers(browser='chrome', os='windows').generate()


response = requests.get('https://habr.com/ru/articles/', headers=get_fake_headers())
soup = bs4.BeautifulSoup(response.text, features='lxml')

preview_list = soup.findAll('article', class_='tm-articles-list__item')
parsed_data = []

for article in preview_list:
    article_link = article.find('a', class_='tm-title__link')['href']
    article_response = requests.get(f'https://habr.com{article_link}', headers=get_fake_headers())
    article = bs4.BeautifulSoup(article_response.text, features='lxml')
    title = article.find('h1').text
    title_lower = title.lower()
    date = article.find('time')['title'][0:10]
    text = article.find('div', class_='article-formatted-body').text
    text_lower = text.lower() # анализируем не только preview-информацию статьи,
    # но и весь текст статьи целиком
    if any(map(lambda x: x in title_lower, KEYWORDS)):
        parsed_data.append({
            'date': date,
            'title': title,
            'link': f'https://habr.com{article_link}'
        })
    elif any(map(lambda x: x in text_lower, KEYWORDS)):
        parsed_data.append({
            'date': date,
            'title': title,
            'link': f'https://habr.com{article_link}'
        })
    else:
        pass

pprint(parsed_data)
