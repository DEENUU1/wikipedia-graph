import requests
from bs4 import BeautifulSoup
from typing import List, Optional

START_URL = ""
END_URL = ""


def get_content(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)

    return None


def get_urls(content: str) -> List[Optional[str]]:
    result = []

    soup = BeautifulSoup(content, "html.parser")
    links = soup.find_all("a")
    if links:
        for link in links:
            if link["href"].startswith("/wiki/"):
                result.append(f"https://pl.wikipedia.org{link['href']}")

    return result


