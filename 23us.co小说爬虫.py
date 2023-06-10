import requests
from bs4 import BeautifulSoup
import re
import os


class Novel:
    def __init__(self):
        self.title = None
        self.book = None
        self.headers = None
        self.url = None
        self.text = None
        self.result = None
        self.result_dict = None
        self.titlelist=[]
        # self.texts = []
    def sanitize_filename(self, filename: str) -> str:
        illegal_chars = '["*<>:"/\\\|?*]'
        sanitized_name = re.sub(illegal_chars, "", filename)
        return sanitized_name
    def download_html(self, value):
        text = self.text.replace(u'\u00a0', u'')
        current_path = os.path.dirname(os.path.abspath(__file__))

        # 创建 download/cc 文件夹
        download_dir = os.path.join(current_path, 'download')
        cc_dir = os.path.join(download_dir, f'{self.sanitize_filename(self.title)}')
        value=self.sanitize_filename(value)

        if not os.path.exists(cc_dir):
            os.makedirs(cc_dir)

        # 打开文件并写入内容
        with open(os.path.join(cc_dir, f'{value}.txt'), 'w', encoding="utf-8") as f:

            f.write(text)
        self.titlelist.append(f'{value}.txt')

    def conbine_novel(self):
        import os

        # 假设 self.title 是 download 目录下的子目录名，self.titlelist 是该目录下的所有txt文件名列表
        current_path = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(current_path, 'download')
        cc_dir = os.path.join(download_dir, self.sanitize_filename(self.title))

        txt_paths = []  # 存储所有txt文件的绝对路径
        for txt_file in self.titlelist:
            txt_path = os.path.join(cc_dir, txt_file)
            txt_paths.append(txt_path)
        import io

        txt_contents = []  # 存储每个txt文件的内容

        for txt_path in txt_paths:
            with io.open(txt_path, 'r', encoding='utf-8') as f:
                txt_content = f.read()
            txt_contents.append(txt_content)
    def get_html_list(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }
        # self.url = "http://23us.co/html/90/90896/"
        response = requests.get(url=self.url, headers=self.headers)

        encoding = response.encoding if "charset" in response.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
        # text = soup.prettify()
        td_list = soup.find_all('td', class_='L')  # 使用class_来匹配class属性
        links = []
        names = []
        for td in td_list:
            a_tag = td.find('a')  # 获取<td>标签内的<a>标签
            if a_tag:
                link = a_tag['href']  # 获取<a>标签的href属性
                name = a_tag.get_text().strip()  # 获取<a>标签的文本内容

                links.append(link)
                names.append(name)

        self.result_dict = {link: name for link, name in zip(links, names)}

    def get_detail_html(self, link):

        url = f'{self.url}{link}'
        # 发送GET请求，并获取响应
        response = requests.get(url, headers=self.headers)
        encoding = response.encoding if "charset" in response.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
        text = soup.get_text().replace(' ', '').replace('\\n', '')
        # 将响应中的HTML内容输出到控制台

        # 使用正则表达式匹配符合条件的部分

        result = re.search(r"->(\S+?)上一页", text)
        # if result:
        # print(result.group(1))
        self.result = result.group(1).split("->", 1)[1]
        # print(self.result)
        # print(text)
        pattern = r"下一页(.*?)没看完？"

        match = re.search(pattern, text, re.S)

        if match:
            text = match.group(1)
            self.text = text.strip()
            # self.texts.append(self.text)
            print(self.text)
        else:
            print("No match found.")

    def search_list(self, original_string):
        global book_name, link, author_name, author_url, sort_url, type_name
        # import requests
        from urllib.parse import unquote
        # original_string = "斗罗大陆"
        encoded_bytes = original_string.encode('gbk')
        # print(encoded_bytes, 'sssssssssssssssssssssssssssssssss')
        # print(type(encoded_bytes))
        data = {
            'type': 'articlename',
            's': encoded_bytes,
            'submit': ''
        }
        # 构造请求参数

        url = f"http://m.23us.co/s.php"
        # 发送 GET 请求并获取响应
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
            'Referer': 'http://m.23us.co/s.php',
            'Origin': 'http://m.23us.co'
        }
        response = requests.post(url, headers=headers, data=data)
        # print(response.text)
        encoding = response.encoding if "charset" in response.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
        books = soup.find_all('a', class_='blue')
        book_type = soup.find_all('p', class_='line')
        self.book = []
        for typebooks in book_type:
            # book_dict = dict()
            typebooks = str(typebooks)
            # 匹配"/sort/1_1/"
            pattern = r'(?<=href=")(/sort/\d+_\d/)'
            match = re.search(pattern, typebooks)
            if match:
                sort_url = match.group(1)
                # print(sort_url)  # 输出：/sort/1_1/
            # 匹配"[玄幻]"
            pattern = r'(?<=>)\[\w+\](?=<)'
            match = re.search(pattern, typebooks)
            if match:
                type_name = match.group()
                # print(type_name)  # 输出：[玄幻]
            # 匹配"/author/唐家三少"
            pattern = r'(?<=href=")(/author/\w+)"'
            match = re.search(pattern, typebooks)
            if match:
                author_url = match.group(1)
                # print(author_url)  # 输出：/author/唐家三少
                author_name = author_url.split("/")[-1]
                # 输出：唐家三少
                # print(author_name)
            pattern = r'<a class="blue" href="(/book/\d+/)".*>(.*?)</a>.*?<a href="/author/.*?".*>(.*?)</a>'
            result = re.search(pattern, typebooks)

            if result:
                # 获取链接
                link = result.group(1)[:-1]
                # print(link)  # 输出：/book/2923/

                # 获取书名
                book_name = result.group(2)
                # print(book_name)  # 输出：斗罗大陆4终极斗罗（斗罗大陆IV终极斗罗）
            book_dict = {
                book_name: link,
                author_name: author_url,
                type_name: sort_url
            }
            self.book.append(book_dict)
            # print(book_dict)
        # print(self.book)

    def get_a_book(self):
        for i, book in enumerate(self.book):
            first_key = list(book.keys())[0]
            print(f"{i + 1}. {first_key}")

        key = int(input())
        # key = 1
        # self.get_html_list(key)
        # print(list(self.book[0].values())[0])
        # url = f'http://23us.co{list(self.book[0].values())[0]}'
        url = f'http://23us.co{str(list(self.book[key - 1].values())[0])}'
        print(url)
        response = requests.get(url)
        self.title = str(list(self.book[key - 1].keys())[0])
        encoding = response.encoding if "charset" in response.headers.get("content-type", "").lower() else None
        soup = BeautifulSoup(response.content, "html.parser", from_encoding=encoding)
        link = soup.select_one('a.read')
        # print(link['title'], link['href'])
        # print(link['href'])
        self.url = link['href']


def root_html(n1, original_string):
    n1.search_list(original_string)
    n1.get_a_book()
    n1.get_html_list()  # lines 和 names 为一一对应的html文件和标题 做类属性
    for key, value in n1.result_dict.items():
        n1.get_detail_html(key)
        n1.download_html(value)
    # n1.conbine_novel()

if __name__ == '__main__':
    n1 = Novel()
    root_html(n1, original_string='宇宙职业选手')
