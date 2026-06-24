import smtplib
from email.mime.text import MIMEText
from database import search_articles

EMAIL_FROM = "childish1206@gmail.com"
EMAIL_PASSWORD = "nlym plyu znxy ilfq"
EMAIL_TO = "a15687878@gmail.com"

def check_and_notify(keyword):
    articles = search_articles(keyword)

    if not articles:
        print(f"沒有找到包含「{keyword}」的文章")
        return

    body = f"找到 {len(articles)} 篇包含「{keyword}」的文章：\n\n"
    for article in articles:
        id, title, url, source, scraped_at = article
        body += f"- {title}\n  {url}\n\n"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"新聞通知：「{keyword}」相關文章"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"✅ 已發送通知信，包含 {len(articles)} 篇文章")

if __name__ == "__main__":
    check_and_notify("AI")