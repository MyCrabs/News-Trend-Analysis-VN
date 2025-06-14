import gradio as gr
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from underthesea import word_tokenize
import re
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/vnexpress.db")
df = pd.read_sql_query("SELECT * FROM article", conn)
conn.close()

stopwords = set([
    "tôi", "anh", "chị", "em", "bạn", "chúng", "ta", "họ", "mình", "bạn", "nó",
    "này", "kia", "đó", "ấy", "nọ", "này", "đấy", "đây", "đấy", "đó", "này",
    "là", "của", "và", "có", "nhưng", "thì", "lại", "nên", "vẫn", "được", "bị", "phải", "rằng", "nếu", "vì", "khi", "ở",
    "đã", "đang", "sẽ", "đến", "với", "từ", "do", "trong", "ngoài", "trên", "dưới", "theo", "qua", "để", "cũng", "đó", 
    "nữa", "còn", "hay", "hoặc", "mà", "nhé", "thôi", "luôn", "chỉ", "hơn", "kém", "đều",
    "một", "hai", "ba", "nhiều", "ít", "rất", "hơi", "vài", "mỗi", "các", "mọi", "tất", "cả",
    "và", "hoặc", "nhưng", "bởi", "do", "tuy", "dù", "mặc", "dù", "xong", "để", "cũng",
    "gì", "ai", "đâu", "sao", "nào", "khi nào", "tại sao",
    "vâng", "dạ", "ừ", "ờ", "ồ", "à", "á", "ồ", "vậy", "thế", "thật", "ừm", "ơ", "ha", "hả", "à", "nhỉ", "chắc",
    "cái", "việc", "này", "kì", "sự", "lúc", "nơi", "người", "điều", "chuyện", "trường", "thời", "gian", "năm", "tháng"
])

def preprocess_text(text):
    text = re.sub(r"[^\w\s]", " ", text.lower()) # Bo dau cau
    tokens = word_tokenize(text, format="text").split()
    filtered = [word for word in tokens if word not in stopwords and len(word) > 1]
    return " ".join(filtered)

def generate_wordcloud(category):
    sub_df = df[df["category"] == category]
    combined_text = " ".join(sub_df["content"].dropna().tolist())
    processed_text = preprocess_text(combined_text)
    wordcloud = WordCloud(width=800, height=400, background_color="white", font_path="arial.ttf").generate(processed_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"Từ khoá nổi bật - {category}", fontsize=16)
    return fig

categories = sorted(df["category"].dropna().unique().tolist())

gr.Interface(
    fn=generate_wordcloud,
    inputs=gr.Dropdown(choices=categories, label="Chọn chuyên mục báo"),
    outputs=gr.Plot(label="WordCloud"),
    title="Từ khoá nổi bật theo chuyên mục báo VNExpress",
    description="Chọn một chuyên mục để xem trực quan từ khoá nổi bật bằng biểu đồ WordCloud."
).launch()