import schedule
import time
from scraper import scrape_hn, scrape_ithome
from database import create_table,delete_old_articles

def job():
    print(f"\n⏰ 開始自動爬取... {time.strftime('%Y-%m-%d %H:%M:%S')}")
    scrape_hn()
    scrape_ithome()
    delete_old_articles(days=1)
    print("✅ 本次自動爬取完成\n")

def start_scheduler(interval_days=1):
    create_table()
    print(f"🚀 排程啟動，每 {interval_days} 分鐘自動爬取一次")
    print("按 Ctrl+C 可停止排程\n")

    job()

    schedule.every(interval_days).days.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler(interval_days=1)