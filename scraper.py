import requests
from bs4 import BeautifulSoup
from database import insert_article, create_table

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def scrape_hn():
    url = "https://news.ycombinator.com/"
    source = "Hacker News"

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select("tr.athing")

    count = 0
    for item in items:
        title_tag = item.select_one("span.titleline > a")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag.get("href", "")

        if href.startswith("http"):
            article_url = href
        else:
            article_url = "https://news.ycombinator.com/" + href

        insert_article(title, article_url, source)
        count += 1
        print(f"[+] {title[:60]}...")

    print(f"\n✅ 共爬取 {count} 篇文章，來源：{source}")
    return count

def scrape_ithome():
    url = "https://www.ithome.com.tw/"
    source = "iThome"

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.select("a[href*='/news/']")

    count = 0
    seen_urls = set()

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href", "")

        if not title or len(title) < 10:
            continue

        if href.startswith("http"):
            article_url = href
        else:
            article_url = "https://www.ithome.com.tw" + href

        if article_url in seen_urls:
            continue
        seen_urls.add(article_url)


        insert_article(title, article_url, source)
        count += 1
        print(f"[+] {title[:60]}...")

    print(f"\n✅ 共爬取 {count} 篇文章，來源：{source}")
    return count


if __name__ == "__main__":
    create_table()
    scrape_hn()
    scrape_ithome() 