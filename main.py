import argparse
from database import create_table, search_articles, get_all_articles, get_stats,get_article_by_id
from scraper import scrape_hn, scrape_ithome
from exporter import export_to_csv
import webbrowser

def show_articles(articles):
    if not articles:
        print("❌ 沒有找到任何文章")
        return
    print(f"\n{'ID':<5} {'來源':<15} {'標題'}")
    print("-" * 80)
    for article in articles:
        id, title, url, source, scraped_at = article
        print(f"{id:<5} {source:<15} {title[:50]}")
        print(f"     🔗 {url}")
    print(f"\n共 {len(articles)} 筆")

def show_stats():
    total, by_source, latest = get_stats()
    print(f"\n📊 資料庫統計")
    print("-" * 40)
    print(f"總文章數：{total} 篇")
    print(f"\n各來源統計：")
    for source, count in by_source:
        print(f"  {source:<20} {count} 篇")
    if latest:
        print(f"\n最新爬取時間：{latest[0]}")

def main():
    parser = argparse.ArgumentParser(description="新聞爬蟲小工具")
    parser.add_argument("action", choices=["scrape", "list", "search", "export", "stats","open"])  
    parser.add_argument("site", nargs="?", default="hn", choices=["hn", "ithome", "all"], help="指定爬取來源")
    parser.add_argument("--keyword", type=str, help="搜尋關鍵字")
    parser.add_argument("--id", type=int, help="文章ID")

    args = parser.parse_args()

    create_table()

    if args.action == "scrape":
        if args.site == "hn":
            scrape_hn()
        elif args.site == "ithome":
            scrape_ithome()
        elif args.site == "all":
            scrape_hn()
            scrape_ithome()

    elif args.action == "list":
        articles = get_all_articles()
        show_articles(articles)

    elif args.action == "search":
        if not args.keyword:
            print("❌ 請提供關鍵字，例如：python main.py search --keyword Python")
            return
        articles = search_articles(args.keyword)
        show_articles(articles)

    elif args.action == "export":
        export_to_csv()

    elif args.action == "stats":
        show_stats()

    elif args.action == "open":
        if not args.id:
            print("❌ 請提供文章ID，例如：python main.py open --id 5")
            return
        article = get_article_by_id(args.id)
        if not article:
            print(f"❌ 找不到 ID {args.id} 的文章")
            return
        id, title, url, source, scraped_at = article
        print(f"🌐 正在開啟：{title}")
        webbrowser.open(url)    

if __name__ == "__main__":
    main()