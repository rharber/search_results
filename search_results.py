import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from pprint import pprint
import pdfkit


def googleSearch(query):
    g_clean = []
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
        query)
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if(re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean


def search_url(query):
    # return 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(
    #     query)
    return f'https://www.google.com/search?q={query}'


def search_queries(qs):
    for q in qs:
        pprint(googleSearch(q))


def build_results_pdf(qs, group_num):
    urls = []
    for q in qs:
        urls.append(search_url(q))
    pdfkit.from_url(urls, f'out{group_num}.pdf')
