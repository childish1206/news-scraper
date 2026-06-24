from flask import Flask, render_template, request
from database import get_all_articles, search_articles, get_stats

app = Flask(__name__)

@app.route("/")
def index():
    keyword = request.args.get("keyword", "")
    if keyword:
        articles = search_articles(keyword)
    else:
        articles = get_all_articles()

    total, by_source, latest = get_stats()

    return render_template(
        "index.html",
        articles=articles,
        total=total,
        by_source=by_source,
        keyword=keyword
    )

@app.route("/chart-data")
def chart_data():
    from database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(scraped_at) as day, COUNT(*) as count
        FROM articles
        GROUP BY day
        ORDER BY day
    """)
    rows = cursor.fetchall()
    conn.close()
    

    from flask import jsonify
    return jsonify({
        "labels": [row[0] for row in rows],
        "counts": [row[1] for row in rows]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)