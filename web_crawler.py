import re
import uuid
from urllib.parse import urlparse

import nltk
import requests
from bs4 import BeautifulSoup as bs

nltk.download('punkt')


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


def save(contents_map):
    with open(f"index.txt", "w") as index:
        for url, content in contents_map.items():
            filename = uuid.uuid4()
            # сохраняем контент
            with open(f"data/{filename}.html", "w") as file:
                file.write(bs(content, features="html.parser").prettify())
            # добавляем в index.txt
            index.write(f"{filename} : {url}\n")


if __name__ == '__main__':
    url = 'https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%B8%D1%88%D1%82%D0%B8%D0%B0%D0%BD%D1%83_%D0%A0%D0%BE%D0%BD%D0%B0%D0%BB%D0%B4%D1%83'
    contents = parse(url)
    save(contents)
