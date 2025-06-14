# VnExpress News Analysis

Phân tích nội dung báo chí từ VnExpress bằng Python, SQlite và Machine Learning.

## Mục tiêu dự án
Dự án nhằm thu thập, làm sạch và phân tích dữ liệu từ trang báo điện tử VnExpress để:
- Cào dữ liệu từ báo điện tử
- Lưu trữ dữ liệu vào SQLite
- Hiểu xu hướng các bài viết theo chuyên mục
- Phân tích xu hướng từ khóa và trực quan từ khoá nổi bật bằng Wordcloud
- Ứng dụng mô hình học máy (Logistic Regression) để dự đoán chuyên mục từ 1 đoạn văn bản mới

## Công nghệ sử dụng
- Python
- requests, BeautifulSoup
- SQLite
- pandas, matplotlib, , sklearn, underthesea, wordcloud
- Gradio

## Cấu trúc thư mục
- `crawler/`: cào dữ liệu
- `data/`: file SQLite
- `analysis/`: xử lý dữ liệu, trực quan hóa, dự đoán văn bản

