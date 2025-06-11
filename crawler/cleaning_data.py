import re
from datetime import datetime
import json

def parse_time(time_data):
    try:
        # Data ban đầu có dạng "Thứ tư, 11/6/2025, 09:14 (GMT+7)"
        parts = time_data.split(', ')
        data = parts[1] + ' ' + parts[2].replace(' (GMT+7)','')
        data = datetime.strptime(data, "%d/%m/%Y %H:%M")
        return data.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Lỗi parse time: {e}")
        return None
    
def clean_article(articles):
    cleaned_list = []
    for article in articles:
        cleaned = {}
        cleaned["title"] = article.get("title", "").strip()
        cleaned['url'] = article.get('url', '').strip()
        cleaned["time"] = parse_time(article.get("time", "").strip())
        # Làm sạch nội dung (content)
        content = article.get("content", "")
        clean_content = re.sub(r'<[^>]+>', '', content)
        clean_content = re.sub(f'\s+', ' ', clean_content)
        cleaned["content"] = clean_content.strip()
        cleaned_list.append(cleaned)
    return cleaned_list
