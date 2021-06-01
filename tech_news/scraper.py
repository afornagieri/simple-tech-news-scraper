import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
        return response.raise_for_status()
    except requests.HTTPError:
        pass
    except requests.Timeout:
        pass


def remove_spaces_from(list):
    return [string.strip() for string in list if len(string) > 1]


# Requisito 2
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("head > link[rel=canonical]::attr(href)").get()
    title = selector.css("h1.tec--article__header__title ::text").get()
    timestamp = selector.css(
        "div.tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = (
        selector.css("main article .tec--author__info__link::text")
        .get()
        .strip()
        if selector.css("main article .tec--author__info__link::text").get()
        is not None
        else None
    )
    shares_count = (
        int(selector.css("div.tec--toolbar__item::text").get().split()[0])
        if selector.css("div.tec--toolbar__item::text").get() is not None
        else 0
    )
    comments_count = (
        int(selector.css("#js-comments-btn ::attr(data-count)").get())
        if selector.css("#js-comments-btn ::attr(data-count)").get()
        is not None
        else None
    )
    summary = selector.css(
        ".tec--article__body p:first-child *::text"
    ).getall()
    fixed_summary = "".join(summary)
    sources = remove_spaces_from(
        selector.css("div.z--mb-16 div *::text").getall()
    )
    categories = remove_spaces_from(
        selector.css("#js-categories a.tec--badge *::text").getall()
    )

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": fixed_summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 3
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    return selector.css(
        ".tec--list a.tec--card__title__link::attr(href)"
    ).getall()


# Requisito 4
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css(
        "a.tec--btn ::attr(href)"
    ).get()


# Requisito 5
def get_tech_news(amount):
    url = "https://www.tecmundo.com.br/novidades"
    news = []
    while len(news) < amount:
        news_page = fetch(url)
        news_list = scrape_novidades(news_page)
        for news_item in news_list:
            news_url = fetch(news_item)
            news.append(scrape_noticia(news_url))
            if len(news) == amount:
                create_news(news)
                return news
        url = scrape_next_page_link(news_page)
