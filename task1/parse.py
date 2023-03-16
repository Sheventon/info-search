import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs


def parse(url):
    contents = {}
    domain = urlparse(url).scheme + '://' + urlparse(url).netloc

    page_content = requests.get(url).text
    soap = bs(page_content, features="html.parser")
    contents[url] = page_content

    current = 0
    max = 200
    # получем все страницы с главной
    for a in soap.find_all('a', href=True):
        if current == max:
            return contents

        url = a['href']
        if not url.startswith("http"):
            if re.match("(.*#.*)|(.*(.svg|.jpg|.jpeg|.gif|.doc|.pdf|.docx)$)", url.lower()):
                continue
            url = domain + url

        contents[url] = requests.get(url).text
        current += 1

    return contents
