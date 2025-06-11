import requests
from bs4 import BeautifulSoup
import json
import time
from save_to_sqlite import save_article_to_db
from cleaning_data import clean_article
"""Requests: gửi yêu cầu http để lấy html
   Beautiful Soup: Phân tích cấu trúc HTML và lấy data"""

def get_article_link(base_url, num_page, option):
   links = []
   for page in range(1, num_page+1):
      url = f"{base_url}-p{page}"
      print(f"Bắt đầu lấy dữ liệu ở trang thứ {page}:{url}")
      try:
         response = requests.get(url)
         response.raise_for_status()
      except requests.RequestException as e:
         print(e)
         continue         
      soup = BeautifulSoup(response.text, "html.parser")
      titles = soup.select("h2.title-news a[href], h3.title-news a[href]")
      print(f"Tìm được {len(titles)} bài viết ở trang {page}")
      for title in titles:
         link = title["href"]
         if "#box_comment_vne" not in link:
            links.append(link)
      time.sleep(1)
   return links

def get_article_content(url):
   response = requests.get(url)
   article_soup = BeautifulSoup(response.text, "html.parser")
   try:
      title = article_soup.find("h1", class_ = "title-detail").text.strip()
      time_published = article_soup.find("span", class_ = "date").text.strip()
      para_content = article_soup.select("article.fck_detail p")
      content = "\n".join(p.text.strip() for p in para_content if p.text.strip())
   except AttributeError:
         return None
   return {
      "url": url,
      "title": title,
      "time": time_published,
      "content": content
   }

def crawl_vnexpress():
   categories = {"1":'thoi-su',"2":'kinh-doanh',"3":'khoa-hoc-cong-nghe',"4":'bat-dong-san',
               "5":'suc-khoe',"6":'the-thao',"7":'giai-tri',"8":'giao-duc',"9":'du-lich'}
   option = input(f"Bạn chọn thể loại báo nào trong những loại sau:{categories} (Chọn số thứ tự): ")
   if option not in categories.keys():
      print("Lựa chọn không hợp lệ. Vui lòng chạy lại và chọn đúng số từ 1 đến 9.")
      return
   print(f"Bạn đã lựa chọn chủ đề {categories[option]}")
   url = f"https://vnexpress.net/{categories[option]}"
   option_num_pages = int(input(f"Vui lòng chọn số trang muốn lấy dữ liệu: "))
   links = get_article_link(url, num_page=option_num_pages, option=option)
   print(f"Đã lấy {len(links)} links. Bắt đầu cào nội dung ...")
   articles = []
   for i, link in enumerate(links):
      print(f"[{i+1}/{len(links)}] {link}")
      try:
         article = get_article_content(link)
         if article:
            articles.append(article)
      except Exception as e:
         print(f":Lỗi khi xử lí link {link}: {e}")
      time.sleep(1)
   # file_name = f"data/vnexpress_{categories[option]}.json"
   # with open(file_name, "w", encoding='utf-8') as f:
   #    json.dump(articles, f, ensure_ascii=False, indent=2)
   # print(f"Hoàn tất. Dữ liệu đã lưu ở data/{file_name}")
   return articles

if __name__ == "__main__":
   articles = clean_article(crawl_vnexpress())
   save_article_to_db(articles=articles, db_path=r"C:\Users\ADMIN\Desktop\Crawling-News-Project\News-Trend-Analysis-VN\data\vnexpress.db")


   