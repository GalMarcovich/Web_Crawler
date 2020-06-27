import requests
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient

url_MongoClient = "mongodb+srv://gal:dovi140198@cluster0-tb3jj.mongodb.net/<dbname>?retryWrites=true&w=majority"
title_class = "field-item even"
brand_class = "field field-name-field-brand field-type-taxonomy-term-reference field-label-inline clearfix"
rockchip_chipset_class = "field field-name-field-chipset field-type-taxonomy-term-reference field-label-inline clearfix"


# check if the name exist already, if it does we update the values if necessary and if it is new we add it to the DB
def page_metadata(html):
    cluster = MongoClient(url_MongoClient)
    db = cluster["app"]
    collection = db["details"]
    # if the name is None return
    if html.find(class_=title_class) is None:
        return
    title = html.find(class_=title_class).get_text()

    if html.find(class_=brand_class) is None or html.find(class_=brand_class).find('a') is None:
        brand = ""
    else:
        brand = html.find(class_=brand_class).find('a').get_text()

    if html.find(class_=rockchip_chipset_class) is None or html.find(class_=rockchip_chipset_class).find('a') is None:
        rockchip_chipset = ""
    else:
        rockchip_chipset = html.find(class_=rockchip_chipset_class).find('a').get_text()

    result = collection.find_one({"_id": title})
    # new
    if result is None:
        post = {"_id": title, "Brand": brand, "Rockchip Chipset": rockchip_chipset}
        collection.insert_one(post)
    else:
        # check if we need to update
        if brand not in result:
            collection.update_one({"_id": title}, {"$set": {"Brand": brand}})
        elif rockchip_chipset not in result:
            collection.update_one({"_id": title}, {"$set": {"Rockchip Chipset": rockchip_chipset}})


# crawl to the home page and get the path of the second page
def first_page(start_url):
    link_name = 'firmware-downloads'
    page = requests.get(start_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if link_name in link['href']:
            full_path = start_url + link['href']
            return full_path


# get the page of every firmware
def get_firmware_links(second_page_path, start_url):
    result_list = []
    links_page = requests.get(second_page_path)
    soup2 = BeautifulSoup(links_page.content, 'html.parser')
    links = [item.find('a', href=True).get('href') for item in soup2.find_all(class_='views-field views-field-title')]
    for link in links[1:]:
        link = start_url + link.replace('\\', '/')
        print(link)
        result_list.append(link)
    return result_list


# download the zip
def zip_firmware(path):
    zip_url = ""
    page_firmware = requests.get(path)
    soup3 = BeautifulSoup(page_firmware.content, 'html.parser')
    page_metadata(soup3)
    for url in soup3.find_all('a', href=True):
        if '.zip' in url['href']:
            zip_url = url['href']
    if zip_url is "":
        return
    Segments = zip_url.rpartition('/')
    r = requests.get(zip_url)
    with open(Segments[2], "wb") as code:
        code.write(r.content)


# get the next url
def get_all_pages(page):
    url = 'https://www.rockchipfirmware.com/'
    page_html = requests.get(page[0])
    soup4 = BeautifulSoup(page_html.content, 'html.parser')
    if soup4.find(class_="pager-next last").find('a') is None:
        return None
    for detail in soup4.find(class_="pager-next last"):
        return url + detail['href']


# collect all the pages
def get_pages_list(page):
    pages = []
    pages += page
    while True:
        url = get_all_pages(page)
        if url is None:
            break
        pages.append(url)
        page = [url]
    return pages


# the crawling function
def crawl(start_url):
    links = []
    second_page_path = first_page(start_url)
    all_pages = get_pages_list([second_page_path])
    for page in all_pages:
        links += get_firmware_links(page, start_url)
    #[zip_firmware(zip_path) for zip_path in links]
    for i in range(3):
        zip_firmware(links[i])


# main function
def main(start_url):
    crawl(start_url)


if __name__ == "__main__":
    #url = 'https://www.rockchipfirmware.com/'
    main(sys.argv[1])
