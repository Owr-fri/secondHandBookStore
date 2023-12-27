import time
import requests
from lxml import etree
import pymysql


def save_image(dir, name, content):
    import os, time, random
    # 文件扩展名
    ext = os.path.splitext(name)[1]
    # 文件目录
    d = os.path.join("\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-2]) + '/media',
                     os.path.dirname(dir))
    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn = fn + '_%d' % random.randint(0, 100)
    # 重写合成文件名
    name = os.path.join(d, fn + ext)
    if not os.path.exists(d):
        os.makedirs(d)
    try:
        with open(name, "wb") as f:  # 文件写入
            f.write(content)
        return os.path.join(dir, fn + ext)
    except:
        return ""


word = str(input("请输入爬取的分类链接："))
category = str(input("请输入分类ID："))
# word = "Cxiaoshuo/v1"
# category = 3
url = "https://item.kongfz.com/" + word + "/"

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                  'Safari/537.36 '
}

connect = pymysql.connect(host='localhost',
                          user='root',
                          password='020706',
                          db='secondhandbookstore')  # 服务器名,账户,密码,数据库名
cur = connect.cursor()

insert_data_sql = "INSERT INTO books_books values(0,'%s','%s','%s','%s','%s','%s',%s,'%s',%s,'%s','%s',%s,'%s')"

response = requests.get(url, headers=headers)
HTML = etree.HTML(response.text)
# print(response.text)

listBox = HTML.xpath("//div[@id='listBox']/div")
for item in listBox:
    href = item.xpath("./div/a[@class='img-box']/@href")[0]
    child_page_res = requests.get(href, headers=headers)
    child_HTML = etree.HTML(child_page_res.text)
    books_info_box = child_HTML.xpath("//div[@class='detail-con-right']")[0]

    name = child_HTML.xpath("//h1[@class='detail-title']/text()")[0]
    image_src = child_HTML.xpath("//img[@id='mainInmg']/@src")[0]
    author = books_info_box.xpath("./div[1]/div[1]/div[1]/span[2]/a/text()")[0]
    translator = books_info_box.xpath("./div[1]/div[1]/div[1]/span[2]/a[2]/text()")[0] if books_info_box.xpath(
        "./div[1]/div[1]/div[1]/span[2]/a[2]/text()") else ""
    press = books_info_box.xpath("./div[1]/div[1]/div[2]/a/span/text()")[0]

    published_data_box = books_info_box.xpath(".//span[@itemprop='datePublished']")
    edition_box = books_info_box.xpath(".//span[@itemprop='bookEdition']")
    isbn_box = books_info_box.xpath(".//span[@itemprop='isbn']")
    price_box = books_info_box.xpath(".//span[@itemprop='price']")
    page_numbers_box = books_info_box.xpath(".//span[@itemprop='numberofpages']")

    edition = edition_box[0].getnext().xpath("./text()") if edition_box else '1'
    isbn = isbn_box[0].getnext().xpath("./text()")[0] if isbn_box else '0000000000000'
    price = price_box[0].getnext().xpath("./text()") if price_box else '0.00'
    published_data = published_data_box[0].getnext().xpath("./text()") if published_data_box else '2000-01-01'
    page_numbers = page_numbers_box[0].getnext().xpath("./text()") if page_numbers_box else '0'
    describe = " ".join([i.replace(' ', '').replace("\u3000", '').replace('\xa0', '').replace('\n', '') for i in
                         books_info_box.xpath(".//li[@class='jianjie'][1]/text()")[1:]])

    author_desc = " ".join([i.replace(' ', '').replace("\u3000", '').replace('\xa0', '').replace('\n', '') for i in
                            books_info_box.xpath(".//li[@class='jianjie'][2]/text()")[1:]])

    if edition:
        edition = edition[0]
    if price:
        price = price[0]
    if published_data:
        published_data = published_data[0]+"-01"
    if page_numbers:
        page_numbers = page_numbers[0].replace('页', '')

    img_content = requests.get(image_src, headers=headers).content
    image = save_image(f'books/{time.strftime("%Y")}/{time.strftime("%m")}/', image_src.split('/')[-1], img_content)

    print(insert_data_sql % (name, isbn, image, author, translator, press,
                             edition, published_data, page_numbers, describe, price, category,author_desc))
    try:
        cur.execute(insert_data_sql % (name, isbn, image, author, translator, press,
                                   edition, published_data, page_numbers, describe, price, category,author_desc))
    except:
        print(f"书《{name}》数据插入失败！")
    # cur.execute(insert_data_sql % (name, isbn, image, author, translator, press,
    #                                edition, published_data, page_numbers, describe, price, category, author_desc))

cur.close()
connect.close()
