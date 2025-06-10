import requests
from bs4 import BeautifulSoup
import json
import time
"""Requests: gửi yêu cầu http để lấy html
   Beautiful Soup: Phân tích cấu trúc HTML là lấy data"""
   
   
url = "https://vnexpress.net/thoi-su"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
artical_link = soup.find("h3", class_ = "title-news")
link = artical_link.find("a")["href"]

artical_response = requests.get(link)
artical_soup = BeautifulSoup(artical_response.text, "html.parser")
title = artical_soup.find("h1", class_ = "title-detail").text.strip()
time_published = artical_soup.find("span", class_ = "date").text.strip()
para_content = artical_soup.select("article.fck_detail p")
content = "\n".join(p.text.strip() for p in para_content if p.text.strip())
print(content)