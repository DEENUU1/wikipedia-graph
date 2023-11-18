import requests
from bs4 import BeautifulSoup


START_URL = ""
END_URL = ""


def get_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(e)