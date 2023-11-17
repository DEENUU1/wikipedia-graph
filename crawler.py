import requests
from bs4 import BeautifulSoup
from typing import List, Optional


def get_page_content(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    except Exception as e:
        print(e)


def get_links(content: str) -> List[Optional[str]]:
    links = []
    soup = BeautifulSoup(content, "html.parser")
    article = soup.find("div.mw-content-ltr mw-parser-output")
    if article:
        links_obj = article.find_all("a")
        if links_obj:
            if links_obj["href"].startswith("/wiki/"):
                links.append(links_obj["href"])

    return links