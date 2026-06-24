import csv
import os
from database import get_all_articles

def export_to_csv(filename="output.csv"):
    articles = get_all_articles()

    if not articles:
        print("❌ 資料庫沒有資料，請先執行爬蟲")
        return

    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow(["ID", "標題", "網址", "來源", "爬取時間"])

        for article in articles:
            writer.writerow(article)

    print(f"✅ 已匯出 {len(articles)} 筆資料到 {filepath}")
    return filepath

if __name__ == "__main__":
    export_to_csv()