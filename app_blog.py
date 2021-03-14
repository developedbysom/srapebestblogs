import requests
from lxml import html
import csv
import re
import click


def add_quote(a):
    return '"{0}"'.format(a)


def write_to_csv(filename, blog_list):

    headers = ['Title', 'Url', 'Author', 'Date', 'Category', 'Likes']
    with open(filename, 'w', encoding='utf-8', newline="") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for row in blog_list:
            writer.writerow(row)


blog_list_info = []


# @click.command()
# @click.option('--url', default='https://blogs.sap.com/', help='Please provide sap blogs url only')
# @click.option('--category', default='Technical Articles', help='Please provide a blog post category')
# @click.option('--like', default='0', help='Please provide your choice')
def scrape(url):
    resp = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
    )

    tree = html.fromstring(html=resp.text)

    blog_list = tree.xpath('//ul[contains(@class,"contentList")]/li')

    for item in blog_list:
        blog_category = item.xpath(
            './/div[contains(@class,"-user")]//child::span[contains(@class,"__category")]/text()')[0]

        blog_likes = item.xpath(
            './/div[contains(@class,"__right")]/child::div/div[position()=2]/div[contains(@class,"Number")]/text()')[0]

        if blog_category != 'Technical Articles':
            continue
        elif blog_category == 'Technical Articles' and int(blog_likes) < 10:
            continue

        blog_url = item.xpath(
            './/div[contains(@class, "__leftContent")]//child::div[contains(@class, "__title")]/a/@href')[0]
        blog_title = item.xpath(
            './/div/div[contains(@class,"_body")]/div[2]/a/text()')[0]
        blog_author = item.xpath(
            './/div[contains(@class,"-user")]//child::a/text()')[0]

        blog_date = item.xpath(
            './/div[contains(@class,"-user")]//child::span[contains(@class,"__date")]/text()')[1]

        blog_info = {
            'Title': blog_title.strip(),
            'Url': blog_url.strip(),
            'Author': blog_author.strip(),
            'Date': blog_date.strip(),
            'Category': blog_category.strip(),
            'Likes': blog_likes.strip()
        }
        blog_list_info.append(blog_info)

    older_post_url = item.xpath(
        '//ul[contains(@class,"pagination-list")]/li/a/span[contains(text(),"Older")]/ancestor::a/@href')[0]

    page_no = re.compile(r"\d+").findall(older_post_url)[0]

    if page_no != '50':
        scrape(url=older_post_url)


scrape(url="https://blogs.sap.com")
write_to_csv('blog.csv', blog_list_info)
