import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint


def get_articles(KEYWORDS: list):
    # Данные строки помогают увидеть динамические данные
    session = HTMLSession()
    response = session.get('https://www.habr.com/ru/all/')
    response.html.render() #Создаем копию страницы с динамическими данными

    # Парсим полученные копию через Beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    for preview_article in articles:
        date = preview_article.find('span', class_='tm-article-snippet__datetime-published').time.get('title')
        href = preview_article.find('h2', class_="tm-article-snippet__title tm-article-snippet__title_h2").a.get('href')
        header = preview_article.find('a', class_='tm-article-snippet__title-link').text
        hubs_list = preview_article.find_all('a', class_="tm-article-snippet__hubs-item-link")
        hubs_list = [hub.text.replace(' *', '') for hub in hubs_list]
        a = set(hubs_list) & set(KEYWORDS)
        if len(set(hubs_list) & set(KEYWORDS)):
            print(f"{date} - {header} - https://www.habr.com{href}")


if __name__ == '__main__':
    KEYWORDS = ['JavaScript', 'C', 'SQL']
    get_articles(KEYWORDS)
