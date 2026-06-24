import sqlite3

DB_NAME = "news.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT NOT NULL,
            url       TEXT UNIQUE NOT NULL,
            source    TEXT,
            scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_article(title, url, source):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO articles (title, url, source)
            VALUES (?, ?, ?)
        """, (title, url, source))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def search_articles(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, source, scraped_at
        FROM articles
        WHERE title LIKE ?
        ORDER BY scraped_at DESC
    """, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_articles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, source, scraped_at
        FROM articles
        ORDER BY scraped_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT source, COUNT(*) as count
        FROM articles
        GROUP BY source
        ORDER BY count DESC
    """)
    by_source = cursor.fetchall()

    cursor.execute("""
        SELECT scraped_at
        FROM articles
        ORDER BY scraped_at DESC
        LIMIT 1
    """)
    latest = cursor.fetchone()

    conn.close()
    return total, by_source, latest


def delete_by_source(source):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE source = ?", (source,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count

def delete_old_articles(days=30):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute("""
        DELETE FROM articles
        WHERE scraped_at < datetime('now', ?)
    """, (f'-{days} days',))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count

def get_article_by_id(article_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, url, source, scraped_at
        FROM articles
        WHERE id = ?
    """, (article_id,))
    row = cursor.fetchone()
    conn.close()
    return row

if __name__ == "__main__":
    create_table()
    print("✅ 資料庫建立成功！")