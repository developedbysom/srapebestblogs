import requests
from lxml import html
import csv


def add_quote(a):
    return '"{0}"'.format(a)


def write_to_csv(filename, blog_list):
    headers = ['title', 'url']
    with open(filename, 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in blog_list:
            # print(row)
            writer.writerow(row)


resp = requests.get(
    url="https://blogs.sap.com/",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
)

tree = html.fromstring(html=resp.text)
blog_item = tree.xpath('//div[contains(@class,"__title")]/a/@href')
# blogs_item = tree.xpath(
#     '//div[contains(@class,"__title")/a[starts-with(@href, "https://blogs.sap.com/2021")]')
blog_list = []
for li in blog_item:
    li_string = add_quote(li)
    xpath_title = '//div[contains(@class, "__title")]' + \
        '/a[@href=' + li_string + ']/text()'
    # print(xpath_title)
    # blog_title = tree.xpath(
    #     '//div[contains(@class,"__title")]/a[@href=li_string]/text()')[0]
    blog_title = tree.xpath(xpath_title)[0]
    blog_tag = tree.xpath('//div[@title="Assigned tags"]/a/text()')
    
    blog_info = {
        'title': blog_title,
        'url': str(li)
    }
    blog_list.append(blog_info)

# print(blog_list)
write_to_csv('blogs.csv', blog_list)
# for row in blog_list:
#     print(row)
