import pickle
import requests
from bs4 import BeautifulSoup
import networkx as nx
from typing import List, Optional
from pyvis.network import Network


def get_page_content(url: str) -> Optional[str]:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    except Exception as e:
        print(e)

    return None


def get_links(content: str) -> List[Optional[str]]:
    links = []
    soup = BeautifulSoup(content, "html.parser")
    article = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if article:
        links_obj = article.find_all("a")
        if links_obj:
            for obj in links_obj:
                if obj.has_attr("href") and obj["href"].startswith("/wiki/"):
                    links.append(f"https://pl.wikipedia.org{obj['href']}")
    return links


def crawl_and_create_graph(starting_url: str) -> nx.Graph:
    graph = nx.Graph()

    graph.add_node(starting_url)

    url_queue = [starting_url]

    count = 0

    while url_queue and count < 5:
        current_url = url_queue.pop(0)

        count += 1

        content = get_page_content(current_url)

        new_links = get_links(content)

        for link in new_links:
            if link not in graph:
                graph.add_node(link)
                graph.add_edge(current_url, link)
                url_queue.append(link)

    with open("wikipedia_daredevil_graph.pkl", "wb") as f:
        pickle.dump(graph, f)

    return graph


if __name__ == "__main__":
    starting_url = "https://pl.wikipedia.org/wiki/Daredevil_(serial_telewizyjny)"

    graph = crawl_and_create_graph(starting_url)

    with open("wikipedia_daredevil_graph.pkl", "rb") as f:
        saved_graph = pickle.load(f)

    vis_net = Network(notebook=True)
    vis_net.from_nx(saved_graph)
    vis_net.show_buttons(filter_=["physics"])
    vis_net.show("Wikipedia_Daredevil_Link_Graph.html")
