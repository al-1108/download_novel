import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from weasyprint import HTML
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
}

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

        # Check if chapter is already in URL
        match = re.search(r"/chapter-(\d+)$", url)

        if match:
            chapter = int(match.group(1))
            return url, chapter

        # If they gave just the novel URL
        if "/novel/" in parsed.path:
            while True:
                chapter = input(
                    "No chapter found. What chapter are you on?: "
                ).strip()

                if chapter.isdigit() and int(chapter) > 0:
                    chapter = int(chapter)
                    return f"{url}/chapter-{chapter}", chapter

                print("Please enter a valid chapter number.")

        print("That doesn't look like a valid novel URL.")

url, start_ch = get_url()
base_url = re.sub(r"/chapter-\d+$", "", url)

chs = int(input("How many chs do you want to download?: "))
end_ch = start_ch + chs - 1

html_content = []
for chapter in range(start_ch, start_ch + chs):
    chapter_url = f"{base_url}/chapter-{chapter}"

    print(f"Downloading chapter {chapter}...")

    try:
        response = requests.get(
            chapter_url,
            headers=headers,
            timeout=5
        )

        if response.status_code == 404:
            print(f"Chapter {chapter} does not exist.")
            end_ch = chapter - 1
            break

        response.raise_for_status()

    except requests.Timeout:
        print(f"Chapter {chapter} timed out.")
        continue

    except requests.ConnectionError:
        print(f"Connection error on chapter {chapter}.")
        continue

    except requests.RequestException as e:
        print(f"Error downloading chapter {chapter}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", id="article")

    if content is None:
        print(f"Could not find article content for chapter {chapter}.")
        continue

    print(f"Chapter {chapter} downloaded successfully.")

    html_content.append(str(content))

    sleep(0.5)

if not html_content:
    print("No chapters were downloaded.")
    exit()

chapters = []

for i, content in enumerate(html_content):
    if i > 0:
        chapters.append('<div class="blank-page">&nbsp;</div>')

    chapters.append(f"""
        <div class="chapter">
            {content}
        </div>
    """)

body_html = ''.join(chapters)

pdf_html = f"""
<html>
<head>
    <meta charset="UTF-8">

    <style>
        body {{
            font-family: serif;
            font-size: 35px;
            line-height: 1.6;
            margin: 0;
        }}

        .blank-page {{
            break-before: page;
            break-after: page;
            height: 1px;
            color: transparent;
        }}
    </style>
</head>

<body>
    {body_html}
</body>
</html>
"""


HTML(string=pdf_html, base_url=base_url).write_pdf(
    f"chapters_{start_ch}-{end_ch}.pdf"
)

print(f"Saved chapters {start_ch}-{end_ch}.")