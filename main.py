import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from time import sleep

url = "https://freewebnovel.com/novel/reverend-insanity/chapter-2334"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
}
response = requests.get(url, headers=headers)
content = BeautifulSoup(response.text, "html.parser").find("div", id="article")
print(content.get_text())

# print(response.status_code)
# response.raise_for_status()
# print(response.text[:1000])