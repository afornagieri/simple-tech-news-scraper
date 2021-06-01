from tech_news.analyzer.search_engine import (
    search_by_date,
    search_by_source,
    search_by_title,
    search_by_category
)
from tech_news.analyzer.ratings import (
    top_5_news,
    top_5_categories
)
from tech_news.scraper import get_tech_news
import sys

menu = [
    "Selecione uma das opções a seguir:\n",
    "0 - Popular o banco com notícias;\n",
    "1 - Buscar notícias por título;\n",
    "2 - Buscar notícias por data;\n",
    "3 - Buscar notícias por fonte;\n",
    "4 - Buscar notícias por categoria;\n",
    "5 - Listar top 5 notícias;\n",
    "6 - Listar top 5 categorias;\n",
    "7 - Sair.\n"]


def search_news():
    qtd_news = int(input('Digite quantas notícias serão buscadas:'))
    return get_tech_news(qtd_news)


def search_news_for__title():
    titulo = input('Digite o título:')
    return search_by_title(titulo)


def search_news_for__date():
    data = input('Digite a data no formato aaaa-mm-dd:')
    return search_by_date(data)


def search_news_for__source():
    fonte = input('Digite a fonte:')
    return search_by_source(fonte)


def search_news_for__category():
    categoria = input('Digite a categoria:')
    return search_by_category(categoria)


def list_five_news():
    return top_5_news()


def list_five_categories():
    return top_5_categories()


def close_app():
    print("Encerrando script\n")


menu_functions = {
    "0": search_news,
    "1": search_news_for__title,
    "2": search_news_for__date,
    "3": search_news_for__source,
    "4": search_news_for__category,
    "5": list_five_news,
    "6": list_five_categories,
    "7": close_app
}


def analyzer_menu():
    global menu
    menu_str = " ".join(menu)
    option = input(menu_str)

    if option in menu_functions:
        return menu_functions[option]()
    else:
        sys.stderr.write('Opção inválida\n')
