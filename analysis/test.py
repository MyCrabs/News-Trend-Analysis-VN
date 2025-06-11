import pandas as pd
import sqlite3

# Kết nối tới database
conn = sqlite3.connect("data/vnexpress.db")
df = pd.read_sql_query("SELECT * FROM article", conn)
conn.close()