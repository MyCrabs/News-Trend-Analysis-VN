import sqlite3

def save_article_to_db(articles, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tạo bảng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        time DATETIME,
        content TEXT,
        link TEXT UNIQUE
        )               
    """)
    
    # Chèn dữ liệu
    for article in articles:
        try:    
            cursor.execute("""
                INSERT OR IGNORE INTO article (title, content, time, link)
                VALUES (?, ?, ?, ?)
            """, (article["title"], article["content"], article["time"], article["url"]))
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vào Database: {e}")
            continue

    conn.commit()
    conn.close()
    print(f"Đã lưu {len(articles)} bài viết vào database: {db_path}")
