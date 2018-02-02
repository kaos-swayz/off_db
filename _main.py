import requests

import bs4 as bs

file_name1 = "url_data.txt"

def unpack_url_data(file_name):
    """ pattern = url_data[0] - base url, url_data[1] - ext url """
    with open(file_name, "r", encoding="UTF-8") as fp:
        url_data = fp.read().split()
    # print(url_data)
    return url_data

def fetch_soup(url):
    session = requests.Session()
    response = session.get(url)
    html = response.content
    soup = bs.BeautifulSoup(html, "lxml")
    return soup

def fetch_links(soup):
    for link in soup.find_all("a", {"class": "rmb-object-list-item"}):
        print("".join(url_data[0] + link.get("href")))

def parse_by_pages(url_data, min_page=0, max_page=9999):
    url = "".join(url_data) + str(min_page)
    fetch_links(fetch_soup(url))


def test_connection(soup):
    print(soup.title)
    print(soup.title.name)
    print(soup.title.string)

if __name__ == "__main__":
    url_data = unpack_url_data("url_data.txt")
    # print("".join(url_data))

    parse_by_pages(url_data)


    # test_connection(soup)