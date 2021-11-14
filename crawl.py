from newspaper import Article  # crawler
import uuid  # generate filename
from bs4 import BeautifulSoup  # parse html
import requests  # get html


# save content to file
def save_file(_filename, _data):
    with open(_filename, 'w') as f:
        f.write(_data)


# crawl content from url
def crawl_content(_url, _filename):
    article = Article(_url)
    article.download()
    article.parse()
    save_file(_filename, article.text)


if __name__ == "__main__":
    # trang chủ dân trí
    url = 'https://dantri.com.vn'
    count = 1  # đếm tổng số bài viết
    # các thể loại báo trong dân trí
    category = ['su-kien', 'xa-hoi', 'the-gioi', 'kinh-doanh', 'bat-dong-san', 'the-thao', 'lao-dong-viec-lam',
                'tam-long-nhan-ai', 'suc-khoe', 'van-hoa', 'giai-tri', 'o-to-xe-may', 'suc-manh-so',
                'giao-duc-huong-nghiep', 'an-sinh', 'phap-luat', 'photo-story', 'du-lich', 'tinh-yeu-gioi-tinh',
                'khoa-hoc-cong-nghe', 'ban-doc', 'doi-song', 'nhip-song-tre', 'blog', 'emagazine', 'infographic']
    for _category in category:
        for page in range(1, 31):
            # cào dữ liệu lưu vào file
            print('Crawling Catagory {} - Page {}'.format(_category, page))
            respone = requests.get("{}/{}/trang-{}.htm".format(url, _category, page))
            soup = BeautifulSoup(respone.text, 'html.parser')
            for child_url in soup.find_all('h3', class_='news-item__title'):
                filename = str(uuid.uuid4())
                print('[{}] - {}'.format(count, child_url.a['href']))
                crawl_content(url + child_url.a['href'], "./data_crawl/{}.story".format(filename))
                count += 1
