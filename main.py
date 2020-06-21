import requests
from bs4 import BeautifulSoup
import sys

# page = requests.get('https://forecast.weather.gov/MapClick.php?lat=39.602&lon=-84.7436#.XuM-qcYzY5k')
# soup = BeautifulSoup(page.content, 'html.parser')
# #print(soup.find_all('a'))
# week = soup.find(id='seven-day-forecast-body')
# #print(week)
# items = week.find_all(class_='tombstone-container')
# #print(items[0])
# '''
# print(items[0].find(class_='period-name').get_text())
# print(items[0].find(class_='short-desc').get_text())
# print(items[0].find(class_='temp').get_text())
# '''
# period_names = [item.find(class_='period-name').get_text() for item in items]
# short_desc = [item.find(class_='short-desc').get_text() for item in items]
# temp = [item.find(class_='temp').get_text() for item in items]
# '''
# print(period_names)
# print(short_desc)
# print(temp)
# '''
#
# weather_stuff = pd.DataFrame(
#     {
#         'period': period_names,
#         'short_desc':short_desc,
#         'temp':temp,
# })

# print(weather_stuff)
# weather_stuff.to_csv('result.csv')

###############################################################################


def page_metadata(start_url):
    return


# crawl to the home page and get the path of the second page
def first_page(start_url):
    link_name = 'firmware-downloads'
    page = requests.get(start_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if link_name in link['href']:
            full_path = start_url + link['href']
            return full_path
    return None


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
    page_frimware = requests.get(path)
    soup3 = BeautifulSoup(page_frimware.content, 'html.parser')
    for url in soup3.find_all('a', href=True):
        if '.zip' in url['href']:
            zip_url = url['href']
    if zip_url is "":
        return
    Segments = zip_url.rpartition('/')
    r = requests.get(zip_url)
    with open(Segments[2], "wb") as code:
        code.write(r.content)


# the crawling function
def crawl(start_url):
    second_page_path = first_page(start_url)
    links_list = get_firmware_links(second_page_path, start_url)
    # r = [zip_firmware(zip_path) for zip_path in links_list]
    # for zip_path in links_list:
    #     zip_firmware(zip_path)
    for i in range(3):
        zip_firmware(links_list[i])
        break

##############################nextpage
def main(start_url):
    crawl(start_url)


# main function
if __name__ == "__main__":
    #url = 'https://www.rockchipfirmware.com/'
    main(sys.argv[1])
