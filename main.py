import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from weasyprint import HTML
from time import sleep

def get_url():
    while True:
        url = input("Enter FreeWebNovel URL: ").strip()

        # Allow user to omit https://
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)

        # Make sure it's actually FreeWebNovel
        if parsed.netloc not in ("freewebnovel.com", "www.freewebnovel.com"):
            print("Please enter a FreeWebNovel URL.")
            continue

        # Remove trailing /
        url = url.rstrip("/")

        # If chapter is already in URL
        if re.search(r"/chapter-\d+$", url):
            return url

        # If they gave just the novel URL
        if "/novel/" in parsed.path:
            while True:
                chapter = input("No chapter found. What chapter are you on? ").strip()

                if chapter.isdigit() and int(chapter) > 0:
                    return f"{url}/chapter-{chapter}"

                print("Please enter a valid chapter number.")

        print("That doesn't look like a valid novel URL.")

url = get_url()
# url = "https://freewebnovel.com/novel/reverend-insanity/chapter-2334"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
}
response = requests.get(url, headers=headers)
content = BeautifulSoup(response.text, "html.parser").find("div", id="article")
print(content)

pdf_html = f"""
<html>
<head>
    <meta charset="UTF-8">

    <style>
        body {{
            font-family: serif;
            font-size: 14px;
            line-height: 1.6;
            margin: 40px;
        }}
    </style>
</head>

<body>
    {str(content)}
</body>
</html>
"""
HTML(string=pdf_html, base_url=url).write_pdf("chapters2.pdf")