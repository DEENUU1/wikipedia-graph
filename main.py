import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import queue


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
            if link.has_attr("href"):
                if link["href"].startswith("/wiki/"):
                    result.append(f"https://pl.wikipedia.org{link['href']}")

    return result


def find_connection(start_url: str, end_url: str) -> Optional[List[str]]:
    visited = set()
    q = queue.Queue()
    q.put([start_url])

    while not q.empty():
        path = q.get()
        current_url = path[-1]

        if current_url in visited:
            continue
        print(current_url)
        visited.add(current_url)
        content = get_content(current_url)

        if content is not None:
            links = get_urls(content)

            for link in links:
                if link == end_url:
                    return path + [link]

                if link not in visited:
                    q.put(path + [link])

    return None


if __name__ == "__main__":
    START_URL = "https://pl.wikipedia.org/wiki/Polska"
    END_URL = "https://pl.wikipedia.org/wiki/Zbrodnia_przeciwko_ludzko%C5%9Bci"

    result = find_connection(START_URL, END_URL)

    if result:
        print("Connection found:")

        print(f"{' -> '.join(result)}")

    else:
        print(f"There is no connection between {START_URL} and {END_URL}")
